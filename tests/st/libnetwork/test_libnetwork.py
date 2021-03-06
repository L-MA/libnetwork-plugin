# Copyright 2015 Metaswitch Networks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import uuid

from netaddr import IPNetwork
from unittest import skip

from tests.st.test_base import TestBase
from tests.st.utils.constants import DEFAULT_IPV4_POOL_CIDR
from tests.st.utils.docker_host import DockerHost


class LibnetworkTests(TestBase):

    @skip("Not written yet")
    def test_moving_endpoints(self):
        """
        Test moving endpoints between hosts and containers.
        """
        # with DockerHost('host1') as host1, DockerHost('host2') as host2:
        #     pass
        # Using docker service attach/detach publish/unpublish ls/info
        pass

    @skip("Not written yet")
    def test_endpoint_ids(self):
        """
        Test that endpoint ID provided by docker service publish can be used
        with calicoctl endpoint commands.
        """
        pass

    def test_pool_ip_assignment(self):
        """
        Test that pools can be used to control IP assignment.

        Remove default IPv4 pool.
        Add a new IPv4 pool.
        Create a new container.
        Assert container receives IP from new IPv4 pool.
        """
        with DockerHost('host', dind=False) as host:
            # Remove default pool and add new pool
            ipv4_pool = "10.0.1.0/24"
            host.calicoctl("pool remove %s" % DEFAULT_IPV4_POOL_CIDR)
            host.calicoctl("pool add %s" % ipv4_pool)

            # Setup network and add a container to the network
            network = host.create_network(str(uuid.uuid4()))
            workload = host.create_workload("workload", network=network)

            # Assert the workload's ip came from the new IP pool
            self.assertIn(workload.ip, IPNetwork(ipv4_pool))
