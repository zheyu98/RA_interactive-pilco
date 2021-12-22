
(cl:in-package :asdf)

(defsystem "dcsc_fpga-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :std_msgs-msg
)
  :components ((:file "_package")
    (:file "MopsActuators" :depends-on ("_package_MopsActuators"))
    (:file "_package_MopsActuators" :depends-on ("_package"))
    (:file "MopsSensors" :depends-on ("_package_MopsSensors"))
    (:file "_package_MopsSensors" :depends-on ("_package"))
  ))