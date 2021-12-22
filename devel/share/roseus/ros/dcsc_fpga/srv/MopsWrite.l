;; Auto-generated. Do not edit!


(when (boundp 'dcsc_fpga::MopsWrite)
  (if (not (find-package "DCSC_FPGA"))
    (make-package "DCSC_FPGA"))
  (shadow 'MopsWrite (find-package "DCSC_FPGA")))
(unless (find-package "DCSC_FPGA::MOPSWRITE")
  (make-package "DCSC_FPGA::MOPSWRITE"))
(unless (find-package "DCSC_FPGA::MOPSWRITEREQUEST")
  (make-package "DCSC_FPGA::MOPSWRITEREQUEST"))
(unless (find-package "DCSC_FPGA::MOPSWRITERESPONSE")
  (make-package "DCSC_FPGA::MOPSWRITERESPONSE"))

(in-package "ROS")





(defclass dcsc_fpga::MopsWriteRequest
  :super ros::object
  :slots (_actuators ))

(defmethod dcsc_fpga::MopsWriteRequest
  (:init
   (&key
    ((:actuators __actuators) (instance dcsc_fpga::MopsActuators :init))
    )
   (send-super :init)
   (setq _actuators __actuators)
   self)
  (:actuators
   (&rest __actuators)
   (if (keywordp (car __actuators))
       (send* _actuators __actuators)
     (progn
       (if __actuators (setq _actuators (car __actuators)))
       _actuators)))
  (:serialization-length
   ()
   (+
    ;; dcsc_fpga/MopsActuators _actuators
    (send _actuators :serialization-length)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; dcsc_fpga/MopsActuators _actuators
       (send _actuators :serialize s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; dcsc_fpga/MopsActuators _actuators
     (send _actuators :deserialize buf ptr-) (incf ptr- (send _actuators :serialization-length))
   ;;
   self)
  )

(defclass dcsc_fpga::MopsWriteResponse
  :super ros::object
  :slots (_success _message ))

(defmethod dcsc_fpga::MopsWriteResponse
  (:init
   (&key
    ((:success __success) nil)
    ((:message __message) "")
    )
   (send-super :init)
   (setq _success __success)
   (setq _message (string __message))
   self)
  (:success
   (&optional (__success :null))
   (if (not (eq __success :null)) (setq _success __success)) _success)
  (:message
   (&optional __message)
   (if __message (setq _message __message)) _message)
  (:serialization-length
   ()
   (+
    ;; bool _success
    1
    ;; string _message
    4 (length _message)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; bool _success
       (if _success (write-byte -1 s) (write-byte 0 s))
     ;; string _message
       (write-long (length _message) s) (princ _message s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; bool _success
     (setq _success (not (= 0 (sys::peek buf ptr- :char)))) (incf ptr- 1)
   ;; string _message
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _message (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;;
   self)
  )

(defclass dcsc_fpga::MopsWrite
  :super ros::object
  :slots ())

(setf (get dcsc_fpga::MopsWrite :md5sum-) "e4d7c08e31b1435de7c05d537862ef59")
(setf (get dcsc_fpga::MopsWrite :datatype-) "dcsc_fpga/MopsWrite")
(setf (get dcsc_fpga::MopsWrite :request) dcsc_fpga::MopsWriteRequest)
(setf (get dcsc_fpga::MopsWrite :response) dcsc_fpga::MopsWriteResponse)

(defmethod dcsc_fpga::MopsWriteRequest
  (:response () (instance dcsc_fpga::MopsWriteResponse :init)))

(setf (get dcsc_fpga::MopsWriteRequest :md5sum-) "e4d7c08e31b1435de7c05d537862ef59")
(setf (get dcsc_fpga::MopsWriteRequest :datatype-) "dcsc_fpga/MopsWriteRequest")
(setf (get dcsc_fpga::MopsWriteRequest :definition-)
      "dcsc_fpga/MopsActuators actuators

================================================================================
MSG: dcsc_fpga/MopsActuators
uint8 digital_outputs
float64 voltage0
float64 voltage1
float64 timeout
---
bool success
string message

")

(setf (get dcsc_fpga::MopsWriteResponse :md5sum-) "e4d7c08e31b1435de7c05d537862ef59")
(setf (get dcsc_fpga::MopsWriteResponse :datatype-) "dcsc_fpga/MopsWriteResponse")
(setf (get dcsc_fpga::MopsWriteResponse :definition-)
      "dcsc_fpga/MopsActuators actuators

================================================================================
MSG: dcsc_fpga/MopsActuators
uint8 digital_outputs
float64 voltage0
float64 voltage1
float64 timeout
---
bool success
string message

")



(provide :dcsc_fpga/MopsWrite "e4d7c08e31b1435de7c05d537862ef59")


