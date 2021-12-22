; Auto-generated. Do not edit!


(cl:in-package dcsc_fpga-srv)


;//! \htmlinclude MopsRead-request.msg.html

(cl:defclass <MopsRead-request> (roslisp-msg-protocol:ros-message)
  ()
)

(cl:defclass MopsRead-request (<MopsRead-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MopsRead-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MopsRead-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name dcsc_fpga-srv:<MopsRead-request> is deprecated: use dcsc_fpga-srv:MopsRead-request instead.")))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MopsRead-request>) ostream)
  "Serializes a message object of type '<MopsRead-request>"
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MopsRead-request>) istream)
  "Deserializes a message object of type '<MopsRead-request>"
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MopsRead-request>)))
  "Returns string type for a service object of type '<MopsRead-request>"
  "dcsc_fpga/MopsReadRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MopsRead-request)))
  "Returns string type for a service object of type 'MopsRead-request"
  "dcsc_fpga/MopsReadRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MopsRead-request>)))
  "Returns md5sum for a message object of type '<MopsRead-request>"
  "d795c28c5471b5cffac720eee35784ef")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MopsRead-request)))
  "Returns md5sum for a message object of type 'MopsRead-request"
  "d795c28c5471b5cffac720eee35784ef")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MopsRead-request>)))
  "Returns full string definition for message of type '<MopsRead-request>"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MopsRead-request)))
  "Returns full string definition for message of type 'MopsRead-request"
  (cl:format cl:nil "~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MopsRead-request>))
  (cl:+ 0
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MopsRead-request>))
  "Converts a ROS message object to a list"
  (cl:list 'MopsRead-request
))
;//! \htmlinclude MopsRead-response.msg.html

(cl:defclass <MopsRead-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil)
   (message
    :reader message
    :initarg :message
    :type cl:string
    :initform "")
   (sensors
    :reader sensors
    :initarg :sensors
    :type dcsc_fpga-msg:MopsSensors
    :initform (cl:make-instance 'dcsc_fpga-msg:MopsSensors)))
)

(cl:defclass MopsRead-response (<MopsRead-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MopsRead-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MopsRead-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name dcsc_fpga-srv:<MopsRead-response> is deprecated: use dcsc_fpga-srv:MopsRead-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <MopsRead-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-srv:success-val is deprecated.  Use dcsc_fpga-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <MopsRead-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-srv:message-val is deprecated.  Use dcsc_fpga-srv:message instead.")
  (message m))

(cl:ensure-generic-function 'sensors-val :lambda-list '(m))
(cl:defmethod sensors-val ((m <MopsRead-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-srv:sensors-val is deprecated.  Use dcsc_fpga-srv:sensors instead.")
  (sensors m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MopsRead-response>) ostream)
  "Serializes a message object of type '<MopsRead-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'sensors) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MopsRead-response>) istream)
  "Deserializes a message object of type '<MopsRead-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'message) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'message) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'sensors) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MopsRead-response>)))
  "Returns string type for a service object of type '<MopsRead-response>"
  "dcsc_fpga/MopsReadResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MopsRead-response)))
  "Returns string type for a service object of type 'MopsRead-response"
  "dcsc_fpga/MopsReadResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MopsRead-response>)))
  "Returns md5sum for a message object of type '<MopsRead-response>"
  "d795c28c5471b5cffac720eee35784ef")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MopsRead-response)))
  "Returns md5sum for a message object of type 'MopsRead-response"
  "d795c28c5471b5cffac720eee35784ef")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MopsRead-response>)))
  "Returns full string definition for message of type '<MopsRead-response>"
  (cl:format cl:nil "bool success~%string message~%dcsc_fpga/MopsSensors sensors~%~%~%================================================================================~%MSG: dcsc_fpga/MopsSensors~%Header header~%float64 position0~%float64 position1~%float64 speed~%float64 voltage~%float64 current~%float64 external_voltage~%uint8 digital_inputs~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MopsRead-response)))
  "Returns full string definition for message of type 'MopsRead-response"
  (cl:format cl:nil "bool success~%string message~%dcsc_fpga/MopsSensors sensors~%~%~%================================================================================~%MSG: dcsc_fpga/MopsSensors~%Header header~%float64 position0~%float64 position1~%float64 speed~%float64 voltage~%float64 current~%float64 external_voltage~%uint8 digital_inputs~%~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%string frame_id~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MopsRead-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'sensors))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MopsRead-response>))
  "Converts a ROS message object to a list"
  (cl:list 'MopsRead-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
    (cl:cons ':sensors (sensors msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'MopsRead)))
  'MopsRead-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'MopsRead)))
  'MopsRead-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MopsRead)))
  "Returns string type for a service object of type '<MopsRead>"
  "dcsc_fpga/MopsRead")