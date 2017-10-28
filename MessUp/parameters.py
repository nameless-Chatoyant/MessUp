class StochasticParameter():
    def draw_samples(self, size, random_state=None):
        """
        Draws one or more sample values from the parameter.
        Parameters
        ----------
        size : tuple of int
            Number of sample values by
            dimension.
        random_state : None or np.random.RandomState, optional(default=None)
            A random state to use during the sampling process.
            If None, the libraries global random state will be used.
        Returns
        -------
        out : (size) iterable
            Sampled values. Usually a numpy ndarray of basically any dtype,
            though not strictly limited to numpy arrays.
        """
        random_state = random_state if random_state is not None else ia.current_random_state()
        samples = self._draw_samples(size, random_state)
        ia.forward_random_state(random_state)
        return samples


# class OneOf

# class SomeOf