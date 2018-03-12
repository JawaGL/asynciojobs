from .job import AbstractJob


class Sequence:
    """A Sequence is an object that organizes a set
    of AbstratJobs in a sequence. Its main purpose is to add
    a single `required` relationship per job in the sequence,
    except the first that instead that receives as its `required`
    the sequence's requirements.

    If `scheduler` is passed to the sequence's constructor,
    all the jobs passed to the sequence are added in that scheduler.

    Sequences are not first-class citizens, in the sense that
    the scheduler primarily ignores these objects, only the jobs inside
    the sequence matter.

    However a sequence can be used mostly every place where a job
    could be, either being inserted in an scheduler, added as a
    requirement, and it can have requirements too
    """

    def __init__(self, *sequences_or_jobs, required=None, scheduler=None):
        """
        Expects a list of jobs or sequences as input

        Required jobs can be passed at object-creation time,
        and/or extended later on with `requires()`
        """
        self.jobs = self._flatten(sequences_or_jobs)
        # create the chain of requirements in the sequence
        for previous, next in zip(self.jobs, self.jobs[1:]):
            next.requires(previous)
        # any requirements specified in the constructor
        # actually apply to the first item
        if self.jobs:
            self.jobs[0].requires(required)
        # make all jobs belong in the scheduler if provided
        self.scheduler = scheduler
        if self.scheduler is not None:
            self.scheduler.update(self.jobs)

    @staticmethod
    def _flatten(sequences_or_jobs):
        """
        given an iterable of objects typed either AbstractJob or Sequence
        returns an ordered list of jobs
        """
        result = []
        for x in sequences_or_jobs:
            if x is None:
                continue
            if isinstance(x, AbstractJob):
                result.append(x)
            elif isinstance(x, Sequence):
                result += x.jobs
        return result

    def append(self, *sequences_or_jobs):
        """
        add these jobs or sequences at the end of the present sequence
        """
        if not sequences_or_jobs:
            return
        new_jobs = self._flatten(sequences_or_jobs)
        if self.jobs:
            new_jobs[0].requires(self.jobs[-1])
        self.jobs += new_jobs
        if self.scheduler is not None:
            self.scheduler.update(new_jobs)

    def requires(self, *requirements):
        """
        Adds requirements to the sequence, that is to say,
        so to the first job in the sequence
        """
        if not self.jobs:
            # warning ?
            return
        self.jobs[0].requires(*requirements)
