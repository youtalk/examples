# Copyright 2016 Open Source Robotics Foundation, Inc.
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

from example_interfaces.srv import AddTwoInts

import rclpy


def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('minimal_client')
    cli = node.create_client(AddTwoInts, 'add_two_ints')

    req = AddTwoInts.Request()
    req.a = 41
    req.b = 1
    while not cli.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('service not available, waiting again...')

    cli.call(req)
    # when calling wait for future
    # spin should not be called in the main loop
    cli.wait_for_future()
    # TODO(mikaelarguedas) This is not the final API, and this does not scale
    # for multiple pending requests. This will change once an executor model is implemented
    # In the future the response will not be stored in cli.response
    node.get_logger().info(
        'Result of add_two_ints: for %d + %d = %d' %
        (req.a, req.b, cli.response.sum))

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
