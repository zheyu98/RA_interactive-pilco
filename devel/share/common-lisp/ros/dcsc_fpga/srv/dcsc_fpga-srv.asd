
(cl:in-package :asdf)

(defsystem "dcsc_fpga-srv"
  :depends-on (:roslisp-msg-protocol :roslisp-utils :dcsc_fpga-msg
)
  :components ((:file "_package")
    (:file "Contr" :depends-on ("_package_Contr"))
    (:file "_package_Contr" :depends-on ("_package"))
    (:file "MopsRead" :depends-on ("_package_MopsRead"))
    (:file "_package_MopsRead" :depends-on ("_package"))
    (:file "MopsWrite" :depends-on ("_package_MopsWrite"))
    (:file "_package_MopsWrite" :depends-on ("_package"))
  ))