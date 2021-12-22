; Auto-generated. Do not edit!


(cl:in-package dcsc_fpga-srv)


;//! \htmlinclude Contr-request.msg.html

(cl:defclass <Contr-request> (roslisp-msg-protocol:ros-message)
  ((angle
    :reader angle
    :initarg :angle
    :type cl:float
    :initform 0.0)
   (velocity
    :reader velocity
    :initarg :velocity
    :type cl:float
    :initform 0.0))
)

(cl:defclass Contr-request (<Contr-request>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Contr-request>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Contr-request)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name dcsc_fpga-srv:<Contr-request> is deprecated: use dcsc_fpga-srv:Contr-request instead.")))

(cl:ensure-generic-function 'angle-val :lambda-list '(m))
(cl:defmethod angle-val ((m <Contr-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-srv:angle-val is deprecated.  Use dcsc_fpga-srv:angle instead.")
  (angle m))

(cl:ensure-generic-function 'velocity-val :lambda-list '(m))
(cl:defmethod velocity-val ((m <Contr-request>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-srv:velocity-val is deprecated.  Use dcsc_fpga-srv:velocity instead.")
  (velocity m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Contr-request>) ostream)
  "Serializes a message object of type '<Contr-request>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'angle))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'velocity))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Contr-request>) istream)
  "Deserializes a message object of type '<Contr-request>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'angle) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'velocity) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Contr-request>)))
  "Returns string type for a service object of type '<Contr-request>"
  "dcsc_fpga/ContrRequest")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Contr-request)))
  "Returns string type for a service object of type 'Contr-request"
  "dcsc_fpga/ContrRequest")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Contr-request>)))
  "Returns md5sum for a message object of type '<Contr-request>"
  "42839bbfa364d97af6de75a8d600af96")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Contr-request)))
  "Returns md5sum for a message object of type 'Contr-request"
  "42839bbfa364d97af6de75a8d600af96")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Contr-request>)))
  "Returns full string definition for message of type '<Contr-request>"
  (cl:format cl:nil "float64 angle~%float64 velocity~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Contr-request)))
  "Returns full string definition for message of type 'Contr-request"
  (cl:format cl:nil "float64 angle~%float64 velocity~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Contr-request>))
  (cl:+ 0
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Contr-request>))
  "Converts a ROS message object to a list"
  (cl:list 'Contr-request
    (cl:cons ':angle (angle msg))
    (cl:cons ':velocity (velocity msg))
))
;//! \htmlinclude Contr-response.msg.html

(cl:defclass <Contr-response> (roslisp-msg-protocol:ros-message)
  ((action
    :reader action
    :initarg :action
    :type cl:float
    :initform 0.0))
)

(cl:defclass Contr-response (<Contr-response>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Contr-response>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Contr-response)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name dcsc_fpga-srv:<Contr-response> is deprecated: use dcsc_fpga-srv:Contr-response instead.")))

(cl:ensure-generic-function 'action-val :lambda-list '(m))
(cl:defmethod action-val ((m <Contr-response>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-srv:action-val is deprecated.  Use dcsc_fpga-srv:action instead.")
  (action m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Contr-response>) ostream)
  "Serializes a message object of type '<Contr-response>"
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'action))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Contr-response>) istream)
  "Deserializes a message object of type '<Contr-response>"
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'action) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Contr-response>)))
  "Returns string type for a service object of type '<Contr-response>"
  "dcsc_fpga/ContrResponse")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Contr-response)))
  "Returns string type for a service object of type 'Contr-response"
  "dcsc_fpga/ContrResponse")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Contr-response>)))
  "Returns md5sum for a message object of type '<Contr-response>"
  "42839bbfa364d97af6de75a8d600af96")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Contr-response)))
  "Returns md5sum for a message object of type 'Contr-response"
  "42839bbfa364d97af6de75a8d600af96")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Contr-response>)))
  "Returns full string definition for message of type '<Contr-response>"
  (cl:format cl:nil "float64 action~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Contr-response)))
  "Returns full string definition for message of type 'Contr-response"
  (cl:format cl:nil "float64 action~%~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Contr-response>))
  (cl:+ 0
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Contr-response>))
  "Converts a ROS message object to a list"
  (cl:list 'Contr-response
    (cl:cons ':action (action msg))
))
(cl:defmethod roslisp-msg-protocol:service-request-type ((msg (cl:eql 'Contr)))
  'Contr-request)
(cl:defmethod roslisp-msg-protocol:service-response-type ((msg (cl:eql 'Contr)))
  'Contr-response)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Contr)))
  "Returns string type for a service object of type '<Contr>"
  "dcsc_fpga/Contr")