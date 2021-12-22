; Auto-generated. Do not edit!


(cl:in-package dcsc_fpga-msg)


;//! \htmlinclude MopsActuators.msg.html

(cl:defclass <MopsActuators> (roslisp-msg-protocol:ros-message)
  ((digital_outputs
    :reader digital_outputs
    :initarg :digital_outputs
    :type cl:fixnum
    :initform 0)
   (voltage0
    :reader voltage0
    :initarg :voltage0
    :type cl:float
    :initform 0.0)
   (voltage1
    :reader voltage1
    :initarg :voltage1
    :type cl:float
    :initform 0.0)
   (timeout
    :reader timeout
    :initarg :timeout
    :type cl:float
    :initform 0.0))
)

(cl:defclass MopsActuators (<MopsActuators>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <MopsActuators>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'MopsActuators)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name dcsc_fpga-msg:<MopsActuators> is deprecated: use dcsc_fpga-msg:MopsActuators instead.")))

(cl:ensure-generic-function 'digital_outputs-val :lambda-list '(m))
(cl:defmethod digital_outputs-val ((m <MopsActuators>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-msg:digital_outputs-val is deprecated.  Use dcsc_fpga-msg:digital_outputs instead.")
  (digital_outputs m))

(cl:ensure-generic-function 'voltage0-val :lambda-list '(m))
(cl:defmethod voltage0-val ((m <MopsActuators>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-msg:voltage0-val is deprecated.  Use dcsc_fpga-msg:voltage0 instead.")
  (voltage0 m))

(cl:ensure-generic-function 'voltage1-val :lambda-list '(m))
(cl:defmethod voltage1-val ((m <MopsActuators>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-msg:voltage1-val is deprecated.  Use dcsc_fpga-msg:voltage1 instead.")
  (voltage1 m))

(cl:ensure-generic-function 'timeout-val :lambda-list '(m))
(cl:defmethod timeout-val ((m <MopsActuators>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader dcsc_fpga-msg:timeout-val is deprecated.  Use dcsc_fpga-msg:timeout instead.")
  (timeout m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <MopsActuators>) ostream)
  "Serializes a message object of type '<MopsActuators>"
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'digital_outputs)) ostream)
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'voltage0))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'voltage1))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-double-float-bits (cl:slot-value msg 'timeout))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 32) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 40) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 48) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 56) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <MopsActuators>) istream)
  "Deserializes a message object of type '<MopsActuators>"
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'digital_outputs)) (cl:read-byte istream))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'voltage0) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'voltage1) (roslisp-utils:decode-double-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 32) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 40) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 48) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 56) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'timeout) (roslisp-utils:decode-double-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<MopsActuators>)))
  "Returns string type for a message object of type '<MopsActuators>"
  "dcsc_fpga/MopsActuators")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'MopsActuators)))
  "Returns string type for a message object of type 'MopsActuators"
  "dcsc_fpga/MopsActuators")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<MopsActuators>)))
  "Returns md5sum for a message object of type '<MopsActuators>"
  "546bc7f707f4532234a4955136c8eadc")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'MopsActuators)))
  "Returns md5sum for a message object of type 'MopsActuators"
  "546bc7f707f4532234a4955136c8eadc")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<MopsActuators>)))
  "Returns full string definition for message of type '<MopsActuators>"
  (cl:format cl:nil "uint8 digital_outputs~%float64 voltage0~%float64 voltage1~%float64 timeout~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'MopsActuators)))
  "Returns full string definition for message of type 'MopsActuators"
  (cl:format cl:nil "uint8 digital_outputs~%float64 voltage0~%float64 voltage1~%float64 timeout~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <MopsActuators>))
  (cl:+ 0
     1
     8
     8
     8
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <MopsActuators>))
  "Converts a ROS message object to a list"
  (cl:list 'MopsActuators
    (cl:cons ':digital_outputs (digital_outputs msg))
    (cl:cons ':voltage0 (voltage0 msg))
    (cl:cons ':voltage1 (voltage1 msg))
    (cl:cons ':timeout (timeout msg))
))
