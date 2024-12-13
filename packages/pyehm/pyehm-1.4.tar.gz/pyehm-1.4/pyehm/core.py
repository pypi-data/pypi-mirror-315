import numpy as np

from .utils import EHMNetNode, EHM2NetNode, EHMNet, EHM2Tree, gen_clusters


class EHM:
    """Efficient Hypothesis Management (EHM)

    An implementation of the EHM algorithm, as documented in [EHM1]_.

    """

    @staticmethod
    def construct_net(validation_matrix):
        """Construct the EHM net as per Section 3.1 of [EHM1]_

        Parameters
        ----------
        validation_matrix: :class:`numpy.ndarray`
            An indicator matrix of shape (num_tracks, num_detections + 1) indicating the possible
            (aka. valid) associations between tracks and detections. The first column corresponds
            to the null hypothesis (hence contains all ones).

        Returns
        -------
        : :class:`~.EHMNet`
            The constructed net object
        """
        num_tracks = validation_matrix.shape[0]

        # Initialise net
        root_node = EHMNetNode(layer=-1)  # Root node is at layer -1
        net = EHMNet([root_node], validation_matrix=validation_matrix)

        # A layer in the network is created for each track (not counting the root-node layer)
        num_layers = num_tracks
        for i in range(num_layers):

            # Get list of nodes in previous layer
            parent_nodes = [node for node in net.nodes if node.layer == i - 1]

            # Get indices of hypothesised detections for the track
            v_detections = set(np.flatnonzero(validation_matrix[i, :]))

            # Compute accumulated measurements up to next layer (i+1)
            acc = set()
            for ii in range(i + 1, num_layers):
                acc |= set(np.flatnonzero(validation_matrix[ii, :]))

            # List of nodes in current layer
            children_per_identity = dict()

            # For all nodes in previous layer
            for parent in parent_nodes:

                # Exclude any detections already considered by parent nodes (always include null)
                v_detections_m1 = (v_detections - parent.identity) | {0}

                # Iterate over valid detections
                for j in v_detections_m1:

                    # Identity
                    identity = acc.intersection(parent.identity | {j}) - {0}

                    # Find valid nodes in current layer that have the same identity
                    try:
                        v_children = children_per_identity[tuple(sorted(identity))]
                    except KeyError:
                        v_children = set()

                    # If layer is empty or no valid nodes exist, add new node
                    if not len(v_children):
                        # Create new node
                        child = EHMNetNode(layer=i, identity=identity)
                        # Add node to net
                        net.add_node(child, parent, j)
                        # Add node to list of child nodes
                        try:
                            children_per_identity[tuple(sorted(child.identity))].add(child)
                        except KeyError:
                            children_per_identity[tuple(sorted(child.identity))] = {child}
                    else:
                        # Simply add new edge or update existing one
                        for child in v_children:
                            net.add_edge(parent, child, j)
        return net

    @staticmethod
    def compute_association_probabilities(net, likelihood_matrix):
        """Compute the joint association weights, as described in Section 3.3 of [EHM1]_

        Parameters
        ----------
        net: :class:`~.EHMNet`
            A net object representing the valid joint association hypotheses
        likelihood_matrix: :class:`numpy.ndarray`
            A matrix of shape (num_tracks, num_detections + 1) containing the unnormalised
            likelihoods for all combinations of tracks and detections. The first column corresponds
            to the null hypothesis.

        Returns
        -------
        :class:`numpy.ndarray`
            A matrix of shape (num_tracks, num_detections + 1) containing the normalised
            association probabilities for all combinations of tracks and detecrtons. The first
            column corresponds to the null hypothesis.
        """
        num_tracks, num_detections = likelihood_matrix.shape
        num_nodes = net.num_nodes

        # Compute p_D (Downward-pass) - Eq. (22) of [EHM1]
        p_D = np.zeros((num_nodes,))
        p_D[0] = 1
        for child in net.nodes[1:]:
            c_i = child.ind
            parents = net.get_parents(child)
            for parent in parents:
                p_i = parent.ind
                ids = list(net.edges[(parent, child)])
                p_D[c_i] += np.sum(likelihood_matrix[child.layer, ids] * p_D[p_i])

        # Compute p_U (Upward-pass) - Eq. (23) of [EHM1]
        p_U = np.zeros((num_nodes,))
        p_U[-1] = 1
        for parent in reversed(net.nodes[:-1]):
            p_i = parent.ind
            children = net.get_children(parent)
            for child in children:
                c_i = child.ind
                ids = list(net.edges[(parent, child)])
                p_U[p_i] += np.sum(likelihood_matrix[child.layer, ids] * p_U[c_i])

        # Compute p_DT - Eq. (21) of [EHM1]
        p_DT = np.zeros((num_detections, num_nodes))
        for child in net.nodes:
            c_i = child.ind
            # v_edges = {edge: ids for edge, ids in net.edges.items() if edge[1] == child}
            # for edge, ids in v_edges.items():
            #     p_i = edge[0].ind
            #     for j in ids:
            #         p_DT[j, c_i] += p_D[p_i]
            for parent in net.get_parents(child):
                p_i = parent.ind
                for j in net.edges[(parent, child)]:
                    p_DT[j, c_i] += p_D[p_i]

        # Compute p_T - Eq. (20) of [EHM1]
        p_T = np.ones((num_detections, num_nodes))
        p_T[:, 0] = 0
        for node in net.nodes[1:]:
            n_i = node.ind
            for j in range(num_detections):
                p_T[j, n_i] = p_U[n_i] * likelihood_matrix[node.layer, j] * p_DT[j, n_i]

        # Compute association weights - Eq. (15) of [EHM1]
        a_matrix = np.zeros(likelihood_matrix.shape)
        for i in range(num_tracks):
            node_inds = [n_i for n_i, node in enumerate(net.nodes) if node.layer == i]
            for j in range(num_detections):
                a_matrix[i, j] = np.sum(p_T[j, node_inds])
            # Normalise
            a_matrix[i, :] = a_matrix[i, :] / np.sum(a_matrix[i, :])

        return a_matrix

    @classmethod
    def run(cls, validation_matrix, likelihood_matrix):
        """Run EHM to compute and return association probabilities

        Parameters
        ----------
        validation_matrix : :class:`numpy.ndarray`
            An indicator matrix of shape (num_tracks, num_detections + 1) indicating the possible
            (aka. valid) associations between tracks and detections. The first column corresponds
            to the null hypothesis (hence contains all ones).
        likelihood_matrix: :class:`numpy.ndarray`
            A matrix of shape (num_tracks, num_detections + 1) containing the unnormalised
            likelihoods for all combinations of tracks and detections. The first column corresponds
            to the null hypothesis.

        Returns
        -------
        :class:`numpy.ndarray`
            A matrix of shape (num_tracks, num_detections + 1) containing the normalised
            association probabilities for all combinations of tracks and detections. The first
            column corresponds to the null hypothesis.
        """

        # Cluster tracks into groups that share common detections
        clusters, missed_tracks = gen_clusters(validation_matrix, likelihood_matrix)

        # Initialise the association probabilities matrix.
        assoc_prob_matrix = np.zeros(likelihood_matrix.shape)
        assoc_prob_matrix[missed_tracks, 0] = 1  # Null hypothesis is certain for missed tracks

        # Perform EHM for each cluster
        for cluster in clusters:

            # Extract track and detection indices
            c_tracks = cluster.tracks
            c_detections = cluster.detections

            # Extract validation and likelihood matrices for cluster
            c_validation_matrix = cluster.validation_matrix
            c_likelihood_matrix = cluster.likelihood_matrix

            # Construct the EHM net
            net = cls.construct_net(c_validation_matrix)

            # Compute the association probabilities
            c_assoc_prob_matrix = cls.compute_association_probabilities(net, c_likelihood_matrix)

            # Map the association probabilities to the main matrix
            for i, track in enumerate(c_tracks):
                assoc_prob_matrix[track, c_detections] = c_assoc_prob_matrix[i, :]

        return assoc_prob_matrix


class EHM2(EHM):
    """ Efficient Hypothesis Management 2 (EHM2)

    An implementation of the EHM2 algorithm, as documented in [EHM2]_.
    """

    @classmethod
    def construct_net(cls, validation_matrix):
        """ Construct the EHM net as per Section 4 of [EHM2]_

        Parameters
        ----------
        validation_matrix: :class:`numpy.ndarray`
            An indicator matrix of shape (num_tracks, num_detections + 1) indicating the possible
            (aka. valid) associations between tracks and detections. The first column corresponds
            to the null hypothesis (hence contains all ones).

        Returns
        -------
        : :class:`~.EHMNet`
            The constructed net object

        Raises
        ------
        ValueError
            If the provided ``validation_matrix`` is such that tracks can be divided into separate clusters. See
            the :ref:`Note <note1>` below for work-around.


        .. _note1:

        .. note::
            If the provided ``validation_matrix`` is such that tracks can be divided into separate clusters, this
            method will raise a ValueError exception. To work-around this issue, you can use the
            :func:`~pyehm.utils.gen_clusters` function to first generate individual clusters and then generate a net
            for each cluster, as shown below:

            .. code-block:: python

                from pyehm.core import EHM2
                from pyehm.utils import gen_clusters

                validation_matrix = <Your validation matrix>

                clusters, _ = gen_clusters(validation_matrix)

                nets = []
                for cluster in clusters:
                    nets.append(EHM2.construct_net(cluster.validation_matrix)

        """
        num_tracks = validation_matrix.shape[0]

        # Construct tree
        try:
            tree = cls.construct_tree(validation_matrix)
        except ValueError:
            raise ValueError('The provided validation matrix results in multiple clusters of tracks')

        # Initialise net
        root_node = EHM2NetNode(layer=0, track=0, subnet=0)
        net = EHMNet([root_node], validation_matrix=validation_matrix)

        # Recursively construct next layers
        cls._construct_net_layer(net, tree, 1)

        # Compute and cache nodes per track
        for i in range(num_tracks):
            net.nodes_per_track[i] = [node for node in net.nodes if node.track == i]

        return net

    @classmethod
    def _construct_net_layer(cls, net, tree, layer):

        # Get list of nodes in previous layer of subtree
        try:
            parent_nodes = net.nodes_per_layer_subnet[(layer - 1, tree.subtree)]
        except KeyError:
            parent_nodes = set()

        # Get indices of hypothesised detections for the track
        v_detections = set(np.flatnonzero(net.validation_matrix[tree.track, :]))

        # If this is not an end layer
        if tree.children:

            # Process each subtree
            for child_tree in tree.children:

                # Compute accumulated measurements up to next layer (i+1)
                acc = {0} | child_tree.detections

                # List of nodes in current layer
                children_per_identity = dict()

                # For all nodes in previous layer
                for parent in parent_nodes:

                    # Exclude any detections already considered by parent nodes (always include null)
                    v_detections_m1 = (v_detections - parent.identity) | {0}

                    # Iterate over valid detections
                    for j in v_detections_m1:

                        # Identity
                        identity = acc.intersection(parent.identity | {j}) - {0}

                        # Find valid nodes in current layer that have the same identity
                        try:
                            v_children = children_per_identity[tuple(sorted(identity))]
                        except KeyError:
                            v_children = set()

                        # If layer is empty or no valid nodes exist, add new node
                        if not len(v_children):
                            # Create new node
                            child = EHM2NetNode(layer=layer, subnet=child_tree.subtree, track=child_tree.track,
                                                identity=identity)
                            # Add node to net
                            net.add_node(child, parent, j)
                            # Add node to list of child nodes
                            try:
                                children_per_identity[tuple(sorted(child.identity))].add(child)
                            except KeyError:
                                children_per_identity[tuple(sorted(child.identity))] = {child}
                        else:
                            # Simply add new edge or update existing one
                            for child in v_children:
                                net.add_edge(parent, child, j)
        else:
            # For all nodes in previous layer
            for parent in parent_nodes:

                # Exclude any detections already considered by parent nodes (always include null)
                v_detections_m1 = (v_detections - parent.identity) | {0}

                # Get leaf child, if any
                try:
                    child = next(iter(net.nodes_per_layer_subnet[(layer, tree.subtree)]))
                except (KeyError, StopIteration):
                    child = None

                # Iterate over valid detections
                for j in v_detections_m1:

                    # If layer is empty or no valid node exist, add new node
                    if not child:
                        # Create new node
                        child = EHM2NetNode(layer=layer, subnet=tree.subtree)
                        # Add node to net
                        net.add_node(child, parent, j)
                    else:
                        # Simply add new edge or update existing one
                        net.add_edge(parent, child, j)

        # Create new layers for each sub-tree
        for i, child_tree in enumerate(tree.children):
            cls._construct_net_layer(net, child_tree, layer + 1)

    @staticmethod
    def construct_tree(validation_matrix):
        """ Construct the EHM2 tree as per section 4.3 of [EHM2]_

        Parameters
        ----------
        validation_matrix: :class:`numpy.ndarray`
            An indicator matrix of shape (num_tracks, num_detections + 1) indicating the possible
            (aka. valid) associations between tracks and detections. The first column corresponds
            to the null hypothesis (hence contains all ones).

        Returns
        -------
        : :class:`~.EHM2Tree`
            The constructed tree object

        Raises
        ------
        ValueError
            If the provided ``validation_matrix`` is such that tracks can be divided into separate clusters. See
            the :ref:`Note <note2>` below for work-around.


        .. _note2:

        .. note::
            If the provided ``validation_matrix`` is such that tracks can be divided into separate clusters, this
            method will raise a ValueError exception. To work-around this issue, you can use the
            :func:`~pyehm.utils.gen_clusters` function to first generate individual clusters and then generate a tree
            for each cluster, as shown below:

            .. code-block:: python

                from pyehm.core import EHM2
                from pyehm.utils import gen_clusters

                validation_matrix = <Your validation matrix>

                clusters, _ = gen_clusters(validation_matrix)

                trees = []
                for cluster in clusters:
                    trees.append(EHM2.construct_tree(cluster.validation_matrix)

        """
        num_tracks = validation_matrix.shape[0]

        trees = []
        last_subtree_index = -1
        for i in reversed(range(num_tracks)):
            # Get indices of hypothesised detections for the track (minus the null hypothesis)
            v_detections = set(np.flatnonzero(validation_matrix[i, :])) - {0}

            matched = []
            for j, tree in enumerate(trees):
                if v_detections.intersection(tree.detections):
                    matched.append(j)

            if matched:
                children = [trees[j] for j in matched]
                detections = set()
                for tree in children:
                    detections |= tree.detections
                detections |= v_detections
                subtree_index = np.max([c.subtree for c in children])
                tree = EHM2Tree(i, children, detections, subtree_index)
                trees = [trees[j] for j in range(len(trees)) if j not in matched]
            else:
                children = []
                last_subtree_index += 1
                tree = EHM2Tree(i, children, v_detections, last_subtree_index)
            trees.append(tree)

        if len(trees) > 1:
            raise ValueError('The provided validation matrix results in multiple clusters of tracks')

        tree = trees[0]

        # Reverse subtree indices
        max_subtree_ind = tree.subtree
        for node in tree.nodes:
            node.subtree = max_subtree_ind - node.subtree

        return tree

    @staticmethod
    def compute_association_probabilities(net, likelihood_matrix):
        """ Compute the joint association weights, as described in Section 4.2 of [EHM2]_

        Parameters
        ----------
        net: :class:`~.EHMNet`
            A net object representing the valid joint association hypotheses
        likelihood_matrix: :class:`numpy.ndarray`
            A matrix of shape (num_tracks, num_detections + 1) containing the unnormalised
            likelihoods for all combinations of tracks and detections. The first column corresponds
            to the null hypothesis.

        Returns
        -------
        :class:`numpy.ndarray`
            A matrix of shape (num_tracks, num_detections + 1) containing the normalised
            association probabilities for all combinations of tracks and detecrtons. The first
            column corresponds to the null hypothesis.
        """
        num_tracks, num_detections = likelihood_matrix.shape
        num_nodes = net.num_nodes

        nodes_forwards = net.nodes_forward
        nodes_backwards = list(reversed(nodes_forwards))

        # Precompute valid detections per track
        v_detections_per_track = [set(np.flatnonzero(row)) for row in net.validation_matrix]

        # Compute w_B (Backward-pass) - Eq. (47) of [EHM2]
        w_B = np.zeros((num_nodes,))
        for parent in nodes_backwards:
            p_i = parent.ind

            # If parent is a leaf node
            if parent.track is None:
                w_B[p_i] = 1
                continue

            weight = 0
            v_detections = v_detections_per_track[parent.track] - parent.identity
            for det_ind in v_detections:
                v_children = net.children_per_detection[(parent, det_ind)]
                weight_det = likelihood_matrix[parent.track, det_ind]
                for child in v_children:
                    c_i = child.ind
                    weight_det *= w_B[c_i]
                weight += weight_det
            w_B[p_i] = weight

        # Compute w_F (Forward-pass) - Eq. (49) of [EHM2]
        w_F = np.zeros((num_nodes,))
        w_F[0] = 1
        for parent in nodes_forwards:
            # Skip the leaf nodes
            if parent.track is None:
                continue
            p_i = parent.ind
            v_detections = v_detections_per_track[parent.track] - parent.identity
            for det_ind in v_detections:
                v_children = net.children_per_detection[(parent, det_ind)]
                for child in v_children:
                    if child.track is None:
                        continue
                    c_i = child.ind
                    sibling_inds = list({c.ind for c in v_children} - {child.ind})
                    sibling_weight = np.prod(w_B[sibling_inds]) if len(sibling_inds) > 0 else 1
                    weight = likelihood_matrix[parent.track, det_ind] * w_F[p_i] * sibling_weight
                    w_F[c_i] += weight

        # Compute association probs - Eq. (46) of [EHM2]
        a_matrix = np.zeros(likelihood_matrix.shape)
        for track in range(num_tracks):
            v_detections = v_detections_per_track[track]
            for detection in v_detections:
                for parent in net.nodes_per_track[track]:
                    try:
                        v_children = net.children_per_detection[(parent, detection)]
                    except KeyError:
                        continue
                    weight = likelihood_matrix[track, detection] * w_F[parent.ind]
                    for child in v_children:
                        weight *= w_B[child.ind]
                    a_matrix[track, detection] += weight
            a_matrix[track, :] /= np.sum(a_matrix[track, :])

        return a_matrix
