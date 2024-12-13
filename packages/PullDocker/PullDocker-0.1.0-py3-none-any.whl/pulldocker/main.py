#!/usr/bin/env python3
##
#     Project: PullDocker
# Description: Watch git repositories for Docker compose configuration changes
#      Author: Fabio Castelli (Muflone) <muflone@muflone.com>
#   Copyright: 2024 Fabio Castelli
#     License: GPL-3+
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
##

import logging
import re

from pulldocker.command_line_options import CommandLineOptions
from pulldocker.pulldocker import PullDocker


def main():
    # Get command-line options
    command_line = CommandLineOptions()
    command_line.add_configuration_arguments()
    options = command_line.parse_options()
    logging.basicConfig(level=options.verbose_level,
                        format='%(asctime)s '
                               '%(levelname)-8s '
                               '%(filename)-15s '
                               'line: %(lineno)-5d '
                               '%(funcName)-20s '
                               '%(message)s')
    pulldocker = PullDocker(filename=options.configuration)
    for profile in pulldocker.configuration.get_profiles():
        logging.info(f'Checking profile {profile.name}')
        if profile.status:
            profile.begin()
            repository = profile.repository
            repository.find_head()
            hash_initial = repository.get_hash()
            logging.debug(f'Initial commit with hash {hash_initial}')
            branch = repository.get_branch()

            # Execute git pull on each remote
            remotes = profile.remotes or repository.get_remotes()
            for remote in remotes:
                repository.pull(remote=remote,
                                branch=branch)
            # Compare hash to detect if new changes arrived
            repository.find_head()
            hash_final = repository.get_hash()
            if hash_initial != hash_final:
                logging.debug(f'New commit with hash {hash_final}')
                if profile.tags_regex:
                    # Check the tags
                    for tag_name in repository.get_tags():
                        tag = repository.get_tag(tag_name)
                        if tag.hash == hash_final:
                            if re.match(profile.tags_regex, tag.name):
                                # This tag matches the latest commit
                                logging.debug(f'Found valid tag {tag.name}')
                                break
                    else:
                        logging.debug(f'Skipping tag {tag.name}')
                        continue
                else:
                    tag = None
                # Deploy passing the tag object
                logging.info(f'Making a new deploy for {profile.name}')
                profile.execute(tag=tag)
            else:
                logging.debug('No new commits found')
            profile.end()
        else:
            logging.debug(f'Skipping disabled profile {profile.name}')


if __name__ == '__main__':
    main()
