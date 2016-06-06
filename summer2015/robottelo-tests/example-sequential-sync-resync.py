"""Test utilities for writing Pulp tests

Part of functionalities of Pulp are defined in this module
and have utilities of single repository synchronization, single
sequential repository sync, sequential repository re-sync.

"""
import logging

from robottelo.cli.repository import Repository

LOGGER = logging.getLogger(__name__)


class Pulp(object):
    """Performance Measurement of RH Satellite 6

    Pulp Synchronization functionality

    """
    @classmethod
    def repository_single_sync(cls, repo_id, repo_name, thread_id):
        """Single Synchronization

        :param str repo_id: Repository id to be synchronized
        :param str repo_name: Repository name
        :return: time measure for a single sync
        :rtype: float

        """
        LOGGER.info(
            "Synchronize {0} by thread-{1}:"
            .format(repo_name, thread_id)
        )

        result = Repository.synchronize({
            'id': repo_id
        })

        if result.return_code != 0:
            LOGGER.error(
                "Sync repository {0} by thread-{1} failed!"
                .format(repo_name, thread_id)
            )
            return 0
        LOGGER.info(
            "Sync repository {0} by thread-{1} successful!"
            .format(repo_name, thread_id)
        )
        return cls.get_elapsed_time(result.stderr)

    @classmethod
    def get_elapsed_time(cls, stderr):
        """retrieve time from stderr"""

        # should return only one time point as a single sync
        real_time = ''
        for line in stderr.split('\n'):
            if line.startswith('real'):
                real_time = line
        return 0 if real_time == '' else float(real_time.split(' ')[1])

    @classmethod
    def repository_single_resync(cls, repo_id, repo_name, thread_id):
        """Resync for a repository"""
        LOGGER.info(
            'Resync {0} by thread-{1}:'
            .format(repo_name, thread_id)
        )
        resync_time_result = []
        for count in range(3):
            resync_time_result.append(
                cls.repository_single_sync(repo_id, repo_name, thread_id)
            )
        return resync_time_result

    @classmethod
    def repositories_sequential_sync(cls, repo_list_ids, repo_list_names,
                                     time_initial_sync_dict, sync_time):
        """Sequential Initial Sync

        @para: repo_list_ids would have a list of enabled repository ids
        @para: repo_list_names
        @para: time_initial_sync_dict
        @para: sync_time

        note: synchronize each repository linearly with restoring
        """
        # iterate each repostitory
        for (rid, rname) in zip(repo_list_ids, repo_list_names):
            # for a repo, synchronize 3 times and append time by each iteration
            for count in range(sync_time):
                cls.logger.info("---------------------------------")
                cls.logger.info("Initial Sync Repository: {0} Attempt {1}"
                                .format(rname, count))
                cls.logger.info("---------------------------------")
                if rid not in time_initial_sync_dict.keys():
                    time_initial_sync_dict[rid] = [
                        cls.repository_single_sync(rid, rname)
                    ]
                else:
                    time_initial_sync_dict[rid]\
                        .append(cls.repository_single_sync(rid, rname))
                # restore database everytime after initial synchronization
                cls.logger.info("---------------------------------")
                cls.logger.info("Initial Sync finishes, reset database.")
                cls.logger.info("---------------------------------")
                # StandupPerfTest.restore_from_savepoint()

        return time_initial_sync_dict

    @classmethod
    def repositories_sequential_resync(cls, repo_list_ids, repo_list_names,
                                       time_resync_dict, resync_time):
        """Sequential Resync

        @para: repo_list_ids
        @para: repo_list_names
        @para: time_resync_dict
        @para: resync_time
        """
        # iterate each repository
        for (rid, rname) in zip(repo_list_ids, repo_list_names):
            # synchronize each repository first (dont time)
            cls.logger.info("---------------------------------")
            cls.logger.info("First sync Repository: {}".format(rname))
            cls.logger.info("---------------------------------")
            cls.repository_single_sync(rid, rname)

            # resync each repository for X times
            for count in range(resync_time):
                cls.logger.info("---------------------------------")
                cls.logger.info("ReSync Repository: {0} Attempt {1}"
                                .format(rname, count))
                cls.logger.info("---------------------------------")
                if rid not in time_resync_dict.keys():
                    time_resync_dict[rid] = [
                        cls.repository_single_sync(rid, rname)
                    ]
                else:
                    time_resync_dict[rid]\
                        .append(cls.repository_single_sync(rid, rname))

            # restore database only after resync of one repo is done
            cls.logger.info("---------------------------------")
            cls.logger.info("Resync Repository {} complete, reset database."
                            .format(rname))
            cls.logger.info("---------------------------------")
            # StandupPerfTest.cls.restore_from_savepoint()

        return time_resync_dict
