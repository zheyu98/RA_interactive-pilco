;; Auto-generated. Do not edit!


(when (boundp 'dcsc_fpga::MopsActuators)
  (if (not (find-package "DCSC_FPGA"))
    (make-package "DCSC_FPGA"))
  (shadow 'MopsActuators (find-package "DCSC_FPGA")))
(unless (find-package "DCSC_FPGA::MOPSACTUATORS")
  (make-package "DCSC_FPGA::MOPSACTUATORS"))

(in-package "ROS")
;;//! \htmlinclude MopsActuators.msg.html


(defclass dcsc_fpga::MopsActuators
  :super ros::object
  :slots (_digital_outputs _voltage0 _voltage1 _timeout ))

(defmethod dcsc_fpga::MopsActuators
  (:init
   (&key
    ((:digital_outputs __digital_outputs) 0)
    ((:voltage0 __voltage0) 0.0)
    ((:voltage1 __voltage1) 0.0)
    ((:timeout __timeout) 0.0)
    )
   (send-super :init)
   (setq _digital_outputs (round __digital_outputs))
   (setq _voltage0 (float __voltage0))
   (setq _voltage1 (float __voltage1))
   (setq _timeout (float __timeout))
   self)
  (:digital_outputs
   (&optional __digital_outputs)
   (if __digital_outputs (setq _digital_outputs __digital_outputs)) _digital_outputs)
  (:voltage0
   (&optional __voltage0)
   (if __voltage0 (setq _voltage0 __voltage0)) _voltage0)
  (:voltage1
   (&optional __voltage1)
   (if __voltage1 (setq _voltage1 __voltage1)) _voltage1)
  (:timeout
   (&optional __timeout)
   (if __timeout (setq _timeout __timeout)) _timeout)
  (:serialization-length
   ()
   (+
    ;; uint8 _digital_outputs
    1
    ;; float64 _voltage0
    8
    ;; float64 _voltage1
    8
    ;; float64 _timeout
    8
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; uint8 _digital_outputs
       (write-byte _digital_outputs s)
     ;; float64 _voltage0
       (sys::poke _voltage0 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _voltage1
       (sys::poke _voltage1 (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;; float64 _timeout
       (sys::poke _timeout (send s :buffer) (send s :count) :double) (incf (stream-count s) 8)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; uint8 _digital_outputs
     (setq _digital_outputs (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; float64 _voltage0
     (setq _voltage0 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _voltage1
     (setq _voltage1 (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;; float64 _timeout
     (setq _timeout (sys::peek buf ptr- :double)) (incf ptr- 8)
   ;;
   self)
  )

(setf (get dcsc_fpga::MopsActuators :md5sum-) "546bc7f707f4532234a4955136c8eadc")
(setf (get dcsc_fpga::MopsActuators :datatype-) "dcsc_fpga/MopsActuators")
(setf (get dcsc_fpga::MopsActuators :definition-)
      "uint8 digital_outputs
float64 voltage0
float64 voltage1
float64 timeout

")



(provide :dcsc_fpga/MopsActuators "546bc7f707f4532234a4955136c8eadc")


