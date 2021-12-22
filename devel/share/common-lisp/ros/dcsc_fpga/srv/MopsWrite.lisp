; Auto-generated. Do not edit!


(cl:in-package dcsc_fpga-srv)


;//! \htmlinclude MopsWrite-request.msg.html

(cl:defclass <MopsWrite-request> (roslisp-msg-protocol:ros-message)
  ((actuators
    :reader actuators
    :initarg :actuators
    :type dcsc_fpga-msg:MopsActuators
    :initform (cl:make-instance 'dcsc_fpga-msg:MopsActuators)))
)

(cl:defclass MopsWrite-request (<MopsWrite-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MopsWrite-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MopsWrite-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name dcsc_fpga-srv:<MopsWrite-request> is deprecated: use dcsc_fpga-srv:MopsWrite-request instead.")))

(cl:ensure-generic-function 'actuators-val :lambda-list '(m))
(cl:defmethod actuators-val ((m <MopsWrite-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-srv:actuators-val is deprecated.  Use dcsc_fpga-srv:actuators instead.")
  (actuators m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MopsWrite-request>) ostream)
  "Serializes a message object of type '<MopsWrite-request>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'actuators) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MopsWrite-request>) istream)
  "Deserializes a message object of type '<MopsWrite-request>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'actuators) istream)
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MopsWrite-request>)))
  "Returns string type for a service object of type '<MopsWrite-request>"
  "dcsc_fpga/MopsWriteRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MopsWrite-request)))
  "Returns string type for a service object of type 'MopsWrite-request"
  "dcsc_fpga/MopsWriteRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MopsWrite-request>)))
  "Returns md5sum for a message object of type '<MopsWrite-request>"
  "e4d7c08e31b1435de7c05d537862ef59")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MopsWrite-request)))
  "Returns md5sum for a message object of type 'MopsWrite-request"
  "e4d7c08e31b1435de7c05d537862ef59")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MopsWrite-request>)))
  "Returns full string definition for message of type '<MopsWrite-request>"
  (cl:format cl:nil "dcsc_fpga/MopsActuators actuators~%~%================================================================================~%MSG: dcsc_fpga/MopsActuators~%uint8 digital_outputs~%float64 voltage0~%float64 voltage1~%float64 timeout~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MopsWrite-request)))
  "Returns full string definition for message of type 'MopsWrite-request"
  (cl:format cl:nil "dcsc_fpga/MopsActuators actuators~%~%================================================================================~%MSG: dcsc_fpga/MopsActuators~%uint8 digital_outputs~%float64 voltage0~%float64 voltage1~%float64 timeout~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MopsWrite-request>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'actuators))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MopsWrite-request>))
  "Converts a ROS message object to a list"
  (cl:list 'MopsWrite-request
    (cl:cons ':actuators (actuators msg))
))
;//! \htmlinclude MopsWrite-response.msg.html

(cl:defclass <MopsWrite-response> (roslisp-msg-protocol:ros-message)
  ((success
    :reader success
    :initarg :success
    :type cl:boolean
    :initform cl:nil)
   (message
    :reader message
    :initarg :message
    :type cl:string
    :initform ""))
)

(cl:defclass MopsWrite-response (<MopsWrite-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MopsWrite-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MopsWrite-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name dcsc_fpga-srv:<MopsWrite-response> is deprecated: use dcsc_fpga-srv:MopsWrite-response instead.")))

(cl:ensure-generic-function 'success-val :lambda-list '(m))
(cl:defmethod success-val ((m <MopsWrite-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-srv:success-val is deprecated.  Use dcsc_fpga-srv:success instead.")
  (success m))

(cl:ensure-generic-function 'message-val :lambda-list '(m))
(cl:defmethod message-val ((m <MopsWrite-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-srv:message-val is deprecated.  Use dcsc_fpga-srv:message instead.")
  (message m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MopsWrite-response>) ostream)
  "Serializes a message object of type '<MopsWrite-response>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:if (cl:slot-value msg 'success) 1 0)) ostream)
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'message))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'message))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MopsWrite-response>) istream)
  "Deserializes a message object of type '<MopsWrite-response>"
    (cl:setf (cl:slot-value msg 'success) (cl:not (cl:zerop (cl:read-byte istream))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'message) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'message) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MopsWrite-response>)))
  "Returns string type for a service object of type '<MopsWrite-response>"
  "dcsc_fpga/MopsWriteResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MopsWrite-response)))
  "Returns string type for a service object of type 'MopsWrite-response"
  "dcsc_fpga/MopsWriteResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MopsWrite-response>)))
  "Returns md5sum for a message object of type '<MopsWrite-response>"
  "e4d7c08e31b1435de7c05d537862ef59")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MopsWrite-response)))
  "Returns md5sum for a message object of type 'MopsWrite-response"
  "e4d7c08e31b1435de7c05d537862ef59")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MopsWrite-response>)))
  "Returns full string definition for message of type '<MopsWrite-response>"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MopsWrite-response)))
  "Returns full string definition for message of type 'MopsWrite-response"
  (cl:format cl:nil "bool success~%string message~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MopsWrite-response>))
  (cl:+ 0
     1
     4 (cl:length (cl:slot-value msg 'message))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MopsWrite-response>))
  "Converts a ROS message object to a list"
  (cl:list 'MopsWrite-response
    (cl:cons ':success (success msg))
    (cl:cons ':message (message msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'MopsWrite)))
  'MopsWrite-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'MopsWrite)))
  'MopsWrite-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MopsWrite)))
  "Returns string type for a service object of type '<MopsWrite>"
  "dcsc_fpga/MopsWrite")