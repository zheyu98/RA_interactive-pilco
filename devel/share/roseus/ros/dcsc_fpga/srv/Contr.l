;; Auto-generated. Do not edit!


(when (boundp 'dcsc_fpga::Contr)
  (if (not (find-package "DCSC_FPGA"))
    (make-package "DCSC_FPGA"))
  (shadow 'Contr (find-package "DCSC_FPGA")))
(unless (find-package "DCSC_FPGA::CONTR")
  (make-package "DCSC_FPGA::CONTR"))
(unless (find-package "DCSC_FPGA::CONTRREQUEST")
  (make-package "DCSC_FPGA::CONTRREQUEST"))
(unless (find-package "DCSC_FPGA::CONTRRESPONSE")
  (make-package "DCSC_FPGA::CONTRRESPONSE"))

(in-package "ROS")





(defclass dcsc_fpga::ContrRequest
  :super ros::object
  :slots (_angle _velocity ))

(defmethod dcsc_fpga::ContrRequest
  (:init
   (&key
    ((:angle __angle) 0.0)
    ((:velocity __velocity) 0.0)
    )
   (send-super :init)
   (setq _angle (float __angle))
   (setq _velocity (float __velocity))
   self)
  (:angle
   (&optional __angle)
   (if __angle (setq _angle __angle)) _angle)
  (:velocity
   (&optional __velocity)
   (if __velocity (setq _velocity __velocity)) _velocity)
  (:serialization-length
   ()
   (+
    ;; float64 _angle
    8
    ;; float64 _velocity
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _angle
       (sys::poke _angle (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _velocity
       (sys::poke _velocity (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _angle
     (setq _angle (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _velocity
     (setq _velocity (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(defclass dcsc_fpga::ContrResponse
  :super ros::object
  :slots (_action ))

(defmethod dcsc_fpga::ContrResponse
  (:init
   (&key
    ((:action __action) 0.0)
    )
   (send-super :init)
   (setq _action (float __action))
   self)
  (:action
   (&optional __action)
   (if __action (setq _action __action)) _action)
  (:serialization-length
   ()
   (+
    ;; float64 _action
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float64 _action
       (sys::poke _action (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float64 _action
     (setq _action (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(defclass dcsc_fpga::Contr
  :super ros::object
  :slots ())

(setf (get dcsc_fpga::Contr :md5sum-) "42839bbfa364d97af6de75a8d600af96")
(setf (get dcsc_fpga::Contr :datatype-) "dcsc_fpga/Contr")
(setf (get dcsc_fpga::Contr :request) dcsc_fpga::ContrRequest)
(setf (get dcsc_fpga::Contr :response) dcsc_fpga::ContrResponse)

(defmethod dcsc_fpga::ContrRequest
  (:response () (instance dcsc_fpga::ContrResponse :init)))

(setf (get dcsc_fpga::ContrRequest :md5sum-) "42839bbfa364d97af6de75a8d600af96")
(setf (get dcsc_fpga::ContrRequest :datatype-) "dcsc_fpga/ContrRequest")
(setf (get dcsc_fpga::ContrRequest :definition-)
      "float64 angle
float64 velocity
---
float64 action

")

(setf (get dcsc_fpga::ContrResponse :md5sum-) "42839bbfa364d97af6de75a8d600af96")
(setf (get dcsc_fpga::ContrResponse :datatype-) "dcsc_fpga/ContrResponse")
(setf (get dcsc_fpga::ContrResponse :definition-)
      "float64 angle
float64 velocity
---
float64 action

")



(provide :dcsc_fpga/Contr "42839bbfa364d97af6de75a8d600af96")


