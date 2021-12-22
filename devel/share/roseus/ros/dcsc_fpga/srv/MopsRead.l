;; Auto-generated. Do not edit!


(when (boundp 'dcsc_fpga::MopsRead)
  (if (not (find-package "DCSC_FPGA"))
    (make-package "DCSC_FPGA"))
  (shadow 'MopsRead (find-package "DCSC_FPGA")))
(unless (find-package "DCSC_FPGA::MOPSREAD")
  (make-package "DCSC_FPGA::MOPSREAD"))
(unless (find-package "DCSC_FPGA::MOPSREADREQUEST")
  (make-package "DCSC_FPGA::MOPSREADREQUEST"))
(unless (find-package "DCSC_FPGA::MOPSREADRESPONSE")
  (make-package "DCSC_FPGA::MOPSREADRESPONSE"))

(in-package "ROS")





(defclass dcsc_fpga::MopsReadRequest
  :super ros::object
  :slots ())

(defmethod dcsc_fpga::MopsReadRequest
  (:init
   (&key
    )
   (send-super :init)
   self)
  (:serialization-length
   ()
   (+
    0
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;;
   self)
  )

(defclass dcsc_fpga::MopsReadResponse
  :super ros::object
  :slots (_success _message _sensors ))

(defmethod dcsc_fpga::MopsReadResponse
  (:init
   (&key
    ((:success __success) nil)
    ((:message __message) "")
    ((:sensors __sensors) (instance dcsc_fpga::MopsSensors :init))
    )
   (send-super :init)
   (setq _success __success)
   (setq _message (string __message))
   (setq _sensors __sensors)
   self)
  (:success
   (&optional (__success :null))
   (if (not (eq __success :null)) (setq _success __success)) _success)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:sensors
   (&rest __sensors)
   (if (keywordp (car __sensors))
       (send* _sensors __sensors)
     (progn
       (if __sensors (setq _sensors (car __sensors)))
       _sensors)))
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ;; string _message
    4 (length _message)
    ;; dcsc_fpga/MopsSensors _sensors
    (send _sensors :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;; dcsc_fpga/MopsSensors _sensors
       (send _sensors :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; dcsc_fpga/MopsSensors _sensors
     (send _sensors :deserialize buf ptr-) (incf ptr- (send _sensors :serialization-length))
   ;;
   self)
  )

(defclass dcsc_fpga::MopsRead
  :super ros::object
  :slots ())

(setf (get dcsc_fpga::MopsRead :md5sum-) "d795c28c5471b5cffac720eee35784ef")
(setf (get dcsc_fpga::MopsRead :datatype-) "dcsc_fpga/MopsRead")
(setf (get dcsc_fpga::MopsRead :request) dcsc_fpga::MopsReadRequest)
(setf (get dcsc_fpga::MopsRead :response) dcsc_fpga::MopsReadResponse)

(defmethod dcsc_fpga::MopsReadRequest
  (:response () (instance dcsc_fpga::MopsReadResponse :init)))

(setf (get dcsc_fpga::MopsReadRequest :md5sum-) "d795c28c5471b5cffac720eee35784ef")
(setf (get dcsc_fpga::MopsReadRequest :datatype-) "dcsc_fpga/MopsReadRequest")
(setf (get dcsc_fpga::MopsReadRequest :definition-)
      "---
bool success
string message
dcsc_fpga/MopsSensors sensors


================================================================================
MSG: dcsc_fpga/MopsSensors
Header header
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

(setf (get dcsc_fpga::MopsReadResponse :md5sum-) "d795c28c5471b5cffac720eee35784ef")
(setf (get dcsc_fpga::MopsReadResponse :datatype-) "dcsc_fpga/MopsReadResponse")
(setf (get dcsc_fpga::MopsReadResponse :definition-)
      "---
bool success
string message
dcsc_fpga/MopsSensors sensors


================================================================================
MSG: dcsc_fpga/MopsSensors
Header header
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



(provide :dcsc_fpga/MopsRead "d795c28c5471b5cffac720eee35784ef")


