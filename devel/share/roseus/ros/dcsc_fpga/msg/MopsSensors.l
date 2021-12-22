;; Auto-generated. Do not edit!


(when (boundp 'dcsc_fpga::MopsSensors)
  (if (not (find-package "DCSC_FPGA"))
    (make-package "DCSC_FPGA"))
  (shadow 'MopsSensors (find-package "DCSC_FPGA")))
(unless (find-package "DCSC_FPGA::MOPSSENSORS")
  (make-package "DCSC_FPGA::MOPSSENSORS"))

(in-package "ROS")
;;//! \htmlinclude MopsSensors.msg.html
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass dcsc_fpga::MopsSensors
  :super ros::object
  :slots (_header _position0 _position1 _speed _voltage _current _external_voltage _digital_inputs ))

(defmethod dcsc_fpga::MopsSensors
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:position0 __position0) 0.0)
    ((:position1 __position1) 0.0)
    ((:speed __speed) 0.0)
    ((:voltage __voltage) 0.0)
    ((:current __current) 0.0)
    ((:external_voltage __external_voltage) 0.0)
    ((:digital_inputs __digital_inputs) 0)
    )
   (send-super :init)
   (setq _header __header)
   (setq _position0 (float __position0))
   (setq _position1 (float __position1))
   (setq _speed (float __speed))
   (setq _voltage (float __voltage))
   (setq _current (float __current))
   (setq _external_voltage (float __external_voltage))
   (setq _digital_inputs (round __digital_inputs))
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:position0
   (&optional __position0)
   (if __position0 (setq _position0 __position0)) _position0)
  (:position1
   (&optional __position1)
   (if __position1 (setq _position1 __position1)) _position1)
  (:speed
   (&optional __speed)
   (if __speed (setq _speed __speed)) _speed)
  (:voltage
   (&optional __voltage)
   (if __voltage (setq _voltage __voltage)) _voltage)
  (:current
   (&optional __current)
   (if __current (setq _current __current)) _current)
  (:external_voltage
   (&optional __external_voltage)
   (if __external_voltage (setq _external_voltage __external_voltage)) _external_voltage)
  (:digital_inputs
   (&optional __digital_inputs)
   (if __digital_inputs (setq _digital_inputs __digital_inputs)) _digital_inputs)
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; float64 _position0
    8
    ;; float64 _position1
    8
    ;; float64 _speed
    8
    ;; float64 _voltage
    8
    ;; float64 _current
    8
    ;; float64 _external_voltage
    8
    ;; uint8 _digital_inputs
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; float64 _position0
       (sys::poke _position0 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _position1
       (sys::poke _position1 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _speed
       (sys::poke _speed (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _voltage
       (sys::poke _voltage (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _current
       (sys::poke _current (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _external_voltage
       (sys::poke _external_voltage (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; uint8 _digital_inputs
       (write-byte _digital_inputs s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; float64 _position0
     (setq _position0 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _position1
     (setq _position1 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _speed
     (setq _speed (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _voltage
     (setq _voltage (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _current
     (setq _current (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _external_voltage
     (setq _external_voltage (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; uint8 _digital_inputs
     (setq _digital_inputs (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get dcsc_fpga::MopsSensors :md5sum-) "e19aa551732aa149ac3b2640b0a2a295")
(setf (get dcsc_fpga::MopsSensors :datatype-) "dcsc_fpga/MopsSensors")
(setf (get dcsc_fpga::MopsSensors :definition-)
      "Header header
float64 position0
float64 position1
float64 speed
float64 voltage
float64 current
float64 external_voltage
uint8 digital_inputs

================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
string frame_id

")



(provide :dcsc_fpga/MopsSensors "e19aa551732aa149ac3b2640b0a2a295")


