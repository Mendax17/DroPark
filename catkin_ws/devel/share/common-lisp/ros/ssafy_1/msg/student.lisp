; Auto-generated. Do not edit!


(cl:in-package ssafy_1-msg)


;//! \htmlinclude student.msg.html

(cl:defclass <student> (roslisp-msg-protocol:ros-message)
  ((first_name
    :reader first_name
    :initarg :first_name
    :type cl:string
    :initform "")
   (last_name
    :reader last_name
    :initarg :last_name
    :type cl:string
    :initform "")
   (age
    :reader age
    :initarg :age
    :type cl:fixnum
    :initform 0)
   (score
    :reader score
    :initarg :score
    :type cl:integer
    :initform 0))
)

(cl:defclass student (<student>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <student>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'student)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ssafy_1-msg:<student> is deprecated: use ssafy_1-msg:student instead.")))

(cl:ensure-generic-function 'first_name-val :lambda-list '(m))
(cl:defmethod first_name-val ((m <student>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ssafy_1-msg:first_name-val is deprecated.  Use ssafy_1-msg:first_name instead.")
  (first_name m))

(cl:ensure-generic-function 'last_name-val :lambda-list '(m))
(cl:defmethod last_name-val ((m <student>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ssafy_1-msg:last_name-val is deprecated.  Use ssafy_1-msg:last_name instead.")
  (last_name m))

(cl:ensure-generic-function 'age-val :lambda-list '(m))
(cl:defmethod age-val ((m <student>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ssafy_1-msg:age-val is deprecated.  Use ssafy_1-msg:age instead.")
  (age m))

(cl:ensure-generic-function 'score-val :lambda-list '(m))
(cl:defmethod score-val ((m <student>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ssafy_1-msg:score-val is deprecated.  Use ssafy_1-msg:score instead.")
  (score m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <student>) ostream)
  "Serializes a message object of type '<student>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'first_name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'first_name))
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'last_name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'last_name))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'age)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'score)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'score)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'score)) ostream)
  (cl:write-byte (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'score)) ostream)
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <student>) istream)
  "Deserializes a message object of type '<student>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'first_name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'first_name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'last_name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'last_name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'age)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'score)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 8) (cl:slot-value msg 'score)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 16) (cl:slot-value msg 'score)) (cl:read-byte istream))
    (cl:setf (cl:ldb (cl:byte 8 24) (cl:slot-value msg 'score)) (cl:read-byte istream))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<student>)))
  "Returns string type for a message object of type '<student>"
  "ssafy_1/student")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'student)))
  "Returns string type for a message object of type 'student"
  "ssafy_1/student")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<student>)))
  "Returns md5sum for a message object of type '<student>"
  "f8bfa80ae3c7a93455596d9622ad33a9")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'student)))
  "Returns md5sum for a message object of type 'student"
  "f8bfa80ae3c7a93455596d9622ad33a9")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<student>)))
  "Returns full string definition for message of type '<student>"
  (cl:format cl:nil "string first_name~%string last_name~%uint8 age~%uint32 score~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'student)))
  "Returns full string definition for message of type 'student"
  (cl:format cl:nil "string first_name~%string last_name~%uint8 age~%uint32 score~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <student>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'first_name))
     4 (cl:length (cl:slot-value msg 'last_name))
     1
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <student>))
  "Converts a ROS message object to a list"
  (cl:list 'student
    (cl:cons ':first_name (first_name msg))
    (cl:cons ':last_name (last_name msg))
    (cl:cons ':age (age msg))
    (cl:cons ':score (score msg))
))
