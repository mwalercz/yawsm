class FreeWorkersPicker:
    def pick_best(self, workers):
        return self.get_free_workers(workers)

    def get_free_workers(self, workers):
        return [w for w in workers if not w.has_work()]
