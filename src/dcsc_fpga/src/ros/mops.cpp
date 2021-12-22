using namespace std;

#include <libusb-1.0/libusb.h>
#include "dcsc_fpga/MopsWrite.h"
#include "dcsc_fpga/MopsRead.h"
#include "dcsc_fpga/MopsSensors.h"
#include "dcsc_fpga/usb_utils.h"
#include "ros/ros.h"
#include "std_msgs/String.h"
#include <string.h>
#include <math.h>

FUGIMops mops(0);

double unwrapAngle(double x){
    x = fmod(x,2.0*M_PI);
    if (x < 0.0)
        x += 2.0*M_PI;
    return x - M_PI;
}

bool init()
{
  int status;
  if ((status = mops.write()) != EOK) {
    ROS_ERROR("[mops] Writing failed with status [%s], I/O error [%s]", strerror(status), strerror(mops.write_error()));
    return false;
  }
  mops.actuators.digital_outputs = 1;
  mops.actuators.voltage0 = 0.0;
  mops.actuators.voltage1 = 0.0;
  mops.actuators.timeout = 1.0;
  return true;
}


bool write(dcsc_fpga::MopsWrite::Request &req, dcsc_fpga::MopsWrite::Response &res)
{
  int status;
  mops.actuators.digital_outputs = req.actuators.digital_outputs;
  mops.actuators.voltage0 = req.actuators.voltage0;
  mops.actuators.voltage1 = req.actuators.voltage1;
  mops.actuators.timeout = req.actuators.timeout;
  if ((status = mops.write()) != EOK) {
    res.success = false;
    res.message = ("Writing failed with status [%s], I/O error [%s]", strerror(status), strerror(mops.write_error()));
    return true;
  }
  res.success = true;
  return true;
}

dcsc_fpga::MopsSensors read(dcsc_fpga::MopsSensors &msg)
{
  int status;
  if ((status = mops.read()) != EOK) {
    ROS_ERROR("[mops] Reading failed with status [%s], I/O error [%s]", strerror(status), strerror(mops.read_error()));
    return msg;
  }
  msg.header.stamp = ros::Time::now();
  msg.position0 = unwrapAngle(mops.sensors.position0);
  msg.position1 = mops.sensors.position1;
  msg.speed = mops.sensors.speed;
  msg.voltage = mops.sensors.voltage;
  msg.current = mops.sensors.current;
  msg.digital_inputs = mops.sensors.digital_inputs;
  return msg;
}


int main(int argc, char **argv)
{
  ros::init(argc, argv, "mops");
  ros::NodeHandle n("~");

  bool initialized = false;
  unsigned int count = 0;

  while (!initialized)
  {
    ++ count;
    if (count > 5)
    {
      ROS_ERROR("[mops] Maximum number of attempts to initialize MOPS reached.");
      return 0;
    }
    initialized = init();
  }

  ros::ServiceServer write_service = n.advertiseService("write", write);
  ros::Publisher read_pub = n.advertise<dcsc_fpga::MopsSensors>("read", 10);

  int rate;
  n.param("rate", rate, 100);
  ros::Rate loop_rate(rate);
  ROS_INFO("[mops] Ready to read and write encoders. Rate is %d", rate);

  while (ros::ok())
  {
    dcsc_fpga::MopsSensors msg;
    msg = read(msg);
    read_pub.publish(msg);

    ros::spinOnce();

    loop_rate.sleep();
  }

  return 0;
}
