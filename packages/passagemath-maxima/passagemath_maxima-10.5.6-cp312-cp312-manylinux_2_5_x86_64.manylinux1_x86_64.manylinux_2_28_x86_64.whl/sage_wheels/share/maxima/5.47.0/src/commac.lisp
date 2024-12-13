;; -*-  Mode: Lisp; Package: Maxima; Syntax: Common-Lisp; Base: 10 -*- ;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;;                                                                    ;;;;;
;;;  Copyright (c) 1984,1987 by William Schelter,University of Texas   ;;;;;
;;;     All rights reserved                                            ;;;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(in-package :maxima)

(defmacro defun-prop (f arg &body body)
  (assert (listp f))
  #+gcl (eval-when (eval) (compiler::compiler-def-hook (first f) body))
  `(setf (get ',(first f) ',(second f)) #'(lambda ,arg ,@body)))

;; Should we give this a different name?
(defvar *fortran-print* nil
  "Tells EXPLODEN we are printing numbers for Fortran so include the exponent marker.")

(defun appears (tree var)
  (cond ((equal tree var)
	 (throw 'appears t))
	((atom tree) nil)
	(t  (appears  (car tree) var)
	    (appears (cdr tree)  var)))
  nil)

(defun appears1 (tree var)
  (cond ((eq tree var)
	 (throw 'appears t))
	((atom tree) nil)
	(t
	 (appears (car tree) var)
	 (appears (cdr tree) var)))
  nil)

(defun appears-in (tree var)
  "Yields t if var appears in tree"
  (catch 'appears
    (if (or (symbolp var) (fixnump var))
	(appears1 tree var)
	(appears tree var))))

;; A more portable implementation of ml-typep.  I (rtoy) think it
;; would probably be better to replace uses of
;; ml-typep with the corresponding Common Lisp typep or type-of or
;; subtypep, as appropriate.
(defun ml-typep (x &optional type)
  (cond (type
	 (cl:let ((pred (get type 'ml-typep)))
	   (if pred
	       (funcall pred x)
	       (typep x type))))
	(t
	 (typecase x
	   (cl:cons 'list)
	   (cl:fixnum 'fixnum)
	   (cl:integer 'bignum)
	   (cl:float 'flonum)
	   (cl:number 'number)
	   (cl:array 'array)
	   (cl:hash-table 'hash-table)
	   (t
	    (type-of x))))))

(defprop :extended-number extended-number-p ml-typep)
(defprop array arrayp ml-typep)
(defprop atom  atom ml-typep)

#+(or cmu scl)
(eval-when (:compile-toplevel :load-toplevel :execute)
  (shadow '(cl:compiled-function-p) (find-package :maxima))
)
#+(or cmu scl)
(defun compiled-function-p (x)
  (and (functionp x) (not (symbolp x))
       (not (eval:interpreted-function-p x))))

(defprop compiled-function compiled-function-p ml-typep)
(defprop extended-number extended-number-p ml-typep)
(defprop fixnum fixnump ml-typep)
(defprop list consp ml-typep)
(defprop number numberp ml-typep)
(defprop string stringp ml-typep)
(defprop symbol  symbolp ml-typep)


(defvar *maxima-arrays* nil
  "Trying to track down any functional arrays in maxima")

(defun *array (name maclisp-type &rest dimlist &aux aarray)
  (cond ((member maclisp-type '(readtable obarray) :test #'eq)
	 (error " bad type ~S" maclisp-type)))
  (pushnew name *maxima-arrays*)	;for tracking down old ones.
  (setq aarray (make-array dimlist :initial-element (case maclisp-type
						      (fixnum 0)
						      (flonum 0.0)
						      (otherwise nil))))
  (cond ((null name) aarray)
	((symbolp name)
	 (setf (symbol-array name) aarray)
	 name)
	(t (error "~S is illegal first arg for *array" name))))

;;;    Change maclisp array referencing.
;;;   Idea1: Make changes in the code which will allow the code to still run in maclisp,
;;;yet will allow, with the appropriate macro definitions of array,arraycall, etc,
;;;to put the array into the value-cell.
;;;   Idea2: Make changes in the array referencing of (a dim1 dim2..) to (arraycall nil (symbol-array a) dim1..)
;;;which would then allow expansion into something which is common lisp compatible, for
;;;the day when (a 2 3) no longer is equivalent to (aref (symbol-function a) 2 3).
;;;I.  change (array a typ dim1 dim2..) to expand to (defvar a (make-array (list dim1 dim2 ...) :type typ')
;;;II. change (a dim1 dim2..) to (arraycall nil (symbol-array a) dim1 dim2 ..)
;;;III define
;;(defmacro symbol-array (ar)
;;    `(symbol-function ,ar))
;;(defmacro arraycall (ignore ar &rest dims)
;;  `(aref ,ar ,@ dims))
;;;IV. change array setting to use (setf (arraycall nil ar dim1.. ) val)
;;;which will generate the correct setting code on the lispm and will
;;;still work in maclisp.

(defmacro maxima-error (datum &rest args)
  `(cerror "without any special action" ,datum ,@args))

(defmacro show (&rest l)
  (loop for v in l
	 collecting `(format t "~%The value of ~A is ~A" ',v ,v) into tem
	 finally (return `(progn ,@ tem))))

(defmacro defquote  (fn (aa . oth) &body rest &aux help ans)
  (setq help (intern (format nil "~a-~a" fn '#:aux)))
  (cond ((eq aa '&rest)
	 (setq ans
	       (list
		`(defmacro ,fn (&rest ,(car oth))
		  `(,',help  ',,(car oth)))
		`(defun ,help (,(car oth)) ,@rest))))
	(t (when (member '&rest oth)
	     (error "at present &rest may only occur as first item in a defquote argument"))
	   (setq ans
		 (list
		  `(defmacro ,fn (,aa . other)
		    (setq other (loop for v in other collecting (list 'quote v)))
		    (check-arg other (eql (length other) ,(length oth))
			       ,(format nil "wrong number of args to ~a" fn))
		    `(,',help ',,aa ,@ other))
		  `(defun ,help (,aa ,@ oth) ,@rest)))))
  `(progn ,@ans))


;;the resulting function will translate to defvar and will behave
;;correctly for the evaluator.

;;(defun gg fexpr (ll)
;;       body)
;;(defquote gg (&rest ll)
;;       body)

;;(DEFQUOTE GG ( &rest C)
;; (list  (car c) (second c) ))
;;the big advantage of using the following over defmspec is that it
;;seems to translate more easily, since it is a fn.
;;New functions which wanted quoted arguments should be defined using
;;defquote


(defun onep (x) (eql 1 x))

(defun extended-number-p (x)
  (member (type-of x) '(bignum rational float )))

(defvar *scan-string-buffer*  nil)

(defun macsyma-read-string (a-string &aux answer)
  (cond ((not (or (search "$" a-string :test #'char-equal)
		  (search ";" a-string :test #'char-equal)))
	 (vector-push-extend #\$ a-string)))
  (with-input-from-string (stream a-string)
    (setq answer (third (mread stream)))
    answer))

(defvar *sharp-read-buffer*
  (make-array 140 :element-type ' #.(array-element-type "a") :fill-pointer 0 :adjustable t))

(defun $-read-aux (arg stream &aux (meval-flag t) (*mread-prompt* ""))
  (declare (special *mread-prompt*)
	   (ignore arg))
  (setf (fill-pointer *sharp-read-buffer*) 0)
  (cond ((eql #\$ (peek-char t stream))
	 (tyi stream)
	 (setq meval-flag nil)))
  (with-output-to-string (st *sharp-read-buffer*)
    (let (char)
      (loop while (not (eql char #\$))
	     do
	     (setq char (tyi stream))
	     (write-char char st))))
  (if meval-flag
      (list 'meval* (list 'quote (macsyma-read-string *sharp-read-buffer*)))
      (list 'quote (macsyma-read-string *sharp-read-buffer*))))

(defun x$-cl-macro-read (stream sub-char arg)
  (declare (ignore arg))
  ($-read-aux sub-char stream))

(set-dispatch-macro-character #\# #\$ #'x$-cl-macro-read)

(defvar *macsyma-readtable*)

(defun find-lisp-readtable-for-macsyma ()
  (cond ((and (boundp '*macsyma-readtable*)
	      (readtablep *macsyma-readtable*))
	 *macsyma-readtable*)
	(t (setq *macsyma-readtable* (copy-readtable nil))
	   (set-dispatch-macro-character #\# #\$ 'x$-cl-macro-read *macsyma-readtable*)
	   *macsyma-readtable*)))

(defun set-readtable-for-macsyma ()
  (setq *readtable* (find-lisp-readtable-for-macsyma)))

(defmfun $mkey (variable)
  "($mkey '$demo)==>:demo"
  (intern (string-left-trim "$" (string variable)) 'keyword))

(defmacro arg (x)
  `(narg1 ,x narg-rest-argument))

(defun narg1 (x l &aux tem)
  (cond ((null x) (length l))
	(t (setq tem (nthcdr (1- x) l))
	   (cond ((null tem) (error "arg ~A beyond range ~A " x (length l)))
		 (t (car tem))))))

(defmacro listify (x)
  `(listify1 ,x narg-rest-argument))

(defmacro setarg (i val)
  `(setarg1 ,i ,val narg-rest-argument))

(defun setarg1 (i val l)
  (setf (nth (1- i) l) val)
  val)

(defun listify1 (n narg-rest-argument)
  (cond ((minusp n) (copy-list (last narg-rest-argument (- n))) )
	((zerop n) nil)
	(t (subseq narg-rest-argument 0 n))))

;; This has been replaced by src/defmfun-check.lisp.  I'm leaving this
;; here for now until we finish up fixing everything like using defun
;; for internal functions and updating user-exposed functions to use
;; defmfun instead of defun.
#+nil
(defmacro defmfun (function &body  rest &aux .n.)
  (cond ((and (car rest) (symbolp (car rest)))
	 ;;old maclisp narg syntax
	 (setq .n. (car rest))
	 (setf (car rest)
	       `(&rest narg-rest-argument &aux (, .n. (length narg-rest-argument))))))
  `(progn
    ;; I (rtoy) think we can consider all defmfun's as translated functions.
    (defprop ,function t translated)
    (defun ,function . ,rest)))

;;sample usage
;;(defun foo a (show a )(show (listify a)) (show (arg 3)))

(defmacro defun-maclisp (function &body body &aux .n.)
  (when (typep body '(cons symbol))
    ;;old maclisp narg syntax
    (setq .n. (car body))
    (setf body
          (cons `(&rest narg-rest-argument &aux (, .n. (length narg-rest-argument)))
                (cdr body))))
  `(progn
    ;; I (rtoy) think we can consider all defmfun's as translated functions.
    (defprop ,function t translated)
    (defun ,function . ,body)))

(defun exploden (symb)
  (let* (string)
    (cond ((symbolp symb)
	   (setq string (print-invert-case symb)))
	  ((floatp symb)
	   (setq string (exploden-format-float symb)))
	  ((integerp symb)
	   ;; When obase > 10, prepend leading zero to
	   ;; ensure that output is readable as a number.
	   (let ((leading-digit (if (> *print-base* 10) #\0)))
             (setq string (format nil "~A" symb))
             (setq string (coerce string 'list))
             (if (and leading-digit (not (digit-char-p (car string) 10.)))
		 (setq string (cons leading-digit string)))
             (return-from exploden string)))
	  (t (setq string (format nil "~A" symb))))
    (assert (stringp string))
    (coerce string 'list)))

(defvar *exploden-strip-float-zeros* t) ;; NIL => allow trailing zeros

(defun exploden-format-float (symb)
  (if (or (= $fpprintprec 0) (> $fpprintprec 16.))
    (exploden-format-float-readably-except-special-values symb)
    (exploden-format-float-pretty symb)))

;; Return a readable string, EXCEPT for not-a-number and infinity, if present;
;; for those, return a probably-nonreadable string.
;; This avoids an error from SBCL about trying to readably print those values.

(defun exploden-format-float-readably-except-special-values (x)
  (if (or (float-inf-p x) (float-nan-p x))
    (format nil "~a" x)
    (let ((*print-readably* t))
      (let ((s (prin1-to-string x)))
        ;; Skip the fix up unless we know it's needed for the Lisp implementation.
        #+(or clisp abcl) (fix-up-exponent-in-place s)
        #+ecl (insert-zero-before-exponent s)
        #-(or clisp abcl ecl) s))))

;; (1) If string looks like "n.nnnD0" or "n.nnnd0", return just "n.nnn".
;; (2) Otherwise, replace #\D or #\d (if present) with #\E or #\e, respectively.
;; (3) Otherwise, return S unchanged.

(defun fix-up-exponent-in-place (s)
  (let ((n (length s)) i)
    (if (> n 2)
      (cond
        ((and (or (eql (aref s (- n 2)) #\D) (eql (aref s (- n 2)) #\d)) (eql (aref s (- n 1)) #\0))
         (subseq s 0 (- n 2)))
        ((setq i (position #\D s))
         (setf (aref s i) #\E)
         s)
        ((setq i (position #\d s))
         (setf (aref s i) #\e)
         s)
        (t s))
      s)))

;; Replace "nnnn.Ennn" or "nnn.ennn" with "nnn.0Ennn" or nnn.0ennn", respectively.
;; (Decimal immediately before exponent without intervening digits is
;; explicitly allowed by CLHS; see Section 2.3.1, "Numbers as Tokens".)

(defun insert-zero-before-exponent (s)
  (let ((n (length s)) (i (position #\. s)))
    (if (and i (< i (1- n)))
      (let ((c (aref s (1+ i))))
        (if (or (eql c #\E) (eql c #\e))
          (concatenate 'string (subseq s 0 (1+ i)) "0" (subseq s (1+ i) n))
          s))
    s)))

(defun exploden-format-float-pretty (symb)
  (let ((a (abs symb)) string)
    ;; When printing out something for Fortran, we want to be
    ;; sure to print the exponent marker so that Fortran
    ;; knows what kind of number it is.  It turns out that
    ;; Fortran's exponent markers are the same as Lisp's so
    ;; we just need to make sure the exponent marker is
    ;; printed.
    (if *fortran-print*
        (setq string (cond
                       ;; Strings for non-finite numbers as specified for input in Fortran 2003 spec;
                       ;; they apparently did not exist in earlier versions.
                       ((float-nan-p symb) "NAN")
                       ((float-inf-p symb) (if (< symb 0) "-INF" "INF"))
                       (t (format nil "~e" symb))))
        (multiple-value-bind (form digits)
          (cond
            ((zerop a)
             (values "~,vf" 1))
            ((<= 0.001 a 1e7)
             (let*
               ((integer-log10 (floor (/ (log a) #.(log 10.0))))
                (scale (1+ integer-log10)))
               (if (< scale $fpprintprec)
                 (values "~,vf" (- $fpprintprec scale))
                 (values "~,ve" (1- $fpprintprec)))))
	    ((or (float-inf-p symb) (float-nan-p symb))
             (return-from exploden-format-float-pretty (format nil "~a" symb)))
            (t
              (values "~,ve" (1- $fpprintprec))))

          ;; Call FORMAT using format string chosen above.
          (setq string (format nil form digits a))

          ;; EXPLODEN is often called after NFORMAT, so it doesn't
          ;; usually see a negative argument. I can't guarantee
          ;; a non-negative argument, so handle negative here.
          (if (< symb 0)
            (setq string (concatenate 'string "-" string)))))

    (if *exploden-strip-float-zeros*
      (or (strip-float-zeros string) string)
      string)))

(defun trailing-zeros-regex-f-0 (s)
  (pregexp:pregexp-match-positions '#.(pregexp:pregexp "^(.*\\.[0-9]*[1-9])00*$")
				   s))
(defun trailing-zeros-regex-f-1 (s)
  (pregexp:pregexp-match-positions '#.(pregexp::pregexp "^(.*\\.0)00*$")
				   s))
(defun trailing-zeros-regex-e-0 (s)
  (pregexp:pregexp-match-positions '#.(pregexp:pregexp "^(.*\\.[0-9]*[1-9])00*([^0-9][+-][0-9]*)$")
				   s))
(defun trailing-zeros-regex-e-1 (s)
  (pregexp:pregexp-match-positions '#.(pregexp:pregexp "^(.*\\.0)00*([^0-9][+-][0-9]*)$")
				   s))

;; Return S with trailing zero digits stripped off, or NIL if there are none.
(defun strip-float-zeros (s)
  (let (matches)
    (cond
      ((setq matches (or (trailing-zeros-regex-f-0 s) (trailing-zeros-regex-f-1 s)))
       (let
	   ((group1 (elt matches 1)))
	 (subseq s (car group1) (cdr group1))))
      ((setq matches (or (trailing-zeros-regex-e-0 s) (trailing-zeros-regex-e-1 s)))
       (let*
	   ((group1 (elt matches 1))
            (s1 (subseq s (car group1) (cdr group1)))
            (group2 (elt matches 2))
            (s2 (subseq s (car group2) (cdr group2))))
	 (concatenate 'string s1 s2)))
      (t nil))))

(defun explodec (symb)		;is called for symbols and numbers
  (loop for v in (coerce (print-invert-case symb) 'list)
     collect (intern (string v))))

;;; If the 'string is all the same case, invert the case.  Otherwise,
;;; do nothing.
#-(or scl allegro)
(defun maybe-invert-string-case (string)
  (let ((all-upper t)
	(all-lower t)
	(length (length string)))
    (dotimes (i length)
      (let ((ch (char string i)))
	(when (both-case-p ch)
	  (if (upper-case-p ch)
	      (setq all-lower nil)
	      (setq all-upper nil)))))
    (cond (all-upper
	   (string-downcase string))
	  (all-lower
	   (string-upcase string))
	  (t
	   string))))

#+(or scl allegro)
(defun maybe-invert-string-case (string)
  (cond (#+scl (eq ext:*case-mode* :lower)
	 #+allegro (eq excl:*current-case-mode* :case-sensitive-lower)
	 string)
	(t
	 (let ((all-upper t)
	       (all-lower t)
	       (length (length string)))
	   (dotimes (i length)
	     (let ((ch (aref string i)))
	       (when (both-case-p ch)
		 (if (upper-case-p ch)
		     (setq all-lower nil)
		     (setq all-upper nil)))))
	   (cond (all-upper
		  (string-downcase string))
		 (all-lower
		  (string-upcase string))
		 (t
		  string))))))

(defun intern-invert-case (string)
  ;; Like read-from-string with readtable-case :invert
  ;; Supply package argument in case this function is called
  ;; from outside the :maxima package.
  (intern (maybe-invert-string-case string) :maxima))


#-(or scl allegro)
(let ((local-table (copy-readtable nil)))
  (setf (readtable-case local-table) :invert)
  (defun print-invert-case (sym)
    (let ((*readtable* local-table)
	  (*print-case* :upcase))
      (princ-to-string sym))))

#+(or scl allegro)
(let ((local-table (copy-readtable nil)))
  (unless #+scl (eq ext:*case-mode* :lower)
	  #+allegro (eq excl:*current-case-mode* :case-sensitive-lower)
    (setf (readtable-case local-table) :invert))
  (defun print-invert-case (sym)
    (cond (#+scl (eq ext:*case-mode* :lower)
	   #+allegro (eq excl:*current-case-mode* :case-sensitive-lower)
	   (let ((*readtable* local-table)
		 (*print-case* :downcase))
	     (princ-to-string sym)))
	  (t
	   (let ((*readtable* local-table)
		 (*print-case* :upcase))
	     (princ-to-string sym))))))

(defun implode (list)
  (declare (optimize (speed 3)))
  (intern-invert-case (map 'string #'(lambda (v)
                                       (etypecase v
                                         (character v)
                                         (symbol (char (symbol-name v) 0))
                                         (integer (code-char v))))
                           list)))

;; Note:  symb can also be a number, not just a symbol.
(defun explode (symb)
  (declare (optimize (speed 3)))
  (map 'list #'(lambda (v) (intern (string v))) (format nil "~s" symb)))

;;; return the first character of the name of a symbol or a string or char
(defun get-first-char (symb)
  (declare (optimize (speed 3)))
  (char (string symb) 0))

(defun getchar (symb i)
  (let ((str (string symb)))
    (if (<= 1 i (length str))
	(intern (string (char str (1- i))))
	nil)))

(defun ascii (n)
  (intern (string n)))

(defun maknam (lis)
  (loop for v in lis
     when (symbolp v)
     collecting (char (symbol-name v) 0) into tem
     else
     when (characterp v)
     collecting v into tem
     else do (maxima-error "bad entry")
     finally
     (return (make-symbol (maybe-invert-string-case (coerce tem 'string))))))

;;for those window labels etc. that are wrong type.
;; is not only called for symbols, but also on numbers
(defun flatc (sym)
  (length (explodec sym)))

(defun flatsize (sym &aux (*print-circle* t))
  (length (exploden sym)))

(defmacro safe-zerop (x)
  (if (symbolp x)
      `(and (numberp ,x) (zerop ,x))
      `(let ((.x. ,x))
         (and (numberp .x.) (zerop .x.)))))

(defmacro signp (sym x)
  (cond ((atom x)
	 (let ((test
		(case sym
		  (e `(zerop ,x))
		  (l `(< ,x 0))
		  (le `(<= ,x 0))
		  (g `(> ,x 0))
		  (ge `(>= ,x 0))
		  (n `(not (zerop ,x))))))
	   `(and (numberp ,x) ,test)))
	(t `(let ((.x. ,x))
	     (signp ,sym .x.)))))

(defvar *prompt-on-read-hang* nil)
(defvar *read-hang-prompt* "")

(defun tyi-raw (&optional (stream *standard-input*) eof-option)
  (let ((ch (read-char-no-hang stream nil eof-option)))
    (if ch
	ch
	(progn
	  (when (and *prompt-on-read-hang* *read-hang-prompt*)
	    (princ *read-hang-prompt*)
	    (finish-output *standard-output*))
	  (read-char stream nil eof-option)))))

(defun tyi (&optional (stream *standard-input*) eof-option)
  (let ((ch (tyi-raw stream eof-option)))
    (if (eql ch eof-option)
      ch
      (backslash-check ch stream eof-option))))

; The sequences of characters
; <anything-except-backslash>
;   (<backslash> <newline> | <backslash> <return> | <backslash> <return> <newline>)+
;   <anything>
; are reduced to <anything-except-backslash> <anything> .
; Note that this has no effect on <backslash> <anything-but-newline-or-return> .

(let ((previous-tyi #\a))
  (defun backslash-check (ch stream eof-option)
    (if (eql previous-tyi #\\ )
      (progn (setq previous-tyi #\a) ch)
      (setq previous-tyi
	(if (eql ch #\\ )
	  (let ((next-char (peek-char nil stream nil eof-option)))
	    (if (or (eql next-char #\newline) (eql next-char #\return))
	      (eat-continuations ch stream eof-option)
	      ch))
	  ch))))
  ; We have just read <backslash> and we know the next character is <newline> or <return>.
  ; Eat line continuations until we come to something which doesn't match, or we reach eof.
  (defun eat-continuations (ch stream eof-option)
    (setq ch (tyi-raw stream eof-option))
    (do () ((not (or (eql ch #\newline) (eql ch #\return))))
      (let ((next-char (peek-char nil stream nil eof-option)))
	(if (and (eql ch #\return) (eql next-char #\newline))
	  (tyi-raw stream eof-option)))
      (setq ch (tyi-raw stream eof-option))
      (let ((next-char (peek-char nil stream nil eof-option)))
	(if (and (eql ch #\\ ) (or (eql next-char #\return) (eql next-char #\newline)))
	  (setq ch (tyi-raw stream eof-option))
	  (return-from eat-continuations ch))))
    ch))

(defmfun $timedate (&optional (time (get-universal-time)) tz)
  (cond
    ((and (consp tz) (eq (caar tz) 'rat))
     (setq tz (/ (second tz) (third tz))))
    ((floatp tz)
     (setq tz (rationalize tz))))
  (if tz (setq tz (/ (round tz 1/60) 60)))
  (let*
    ((time-integer (mfuncall '$floor time))
     (time-fraction (sub time time-integer))
     (time-millis (mfuncall '$round (mul 1000 time-fraction))))
    (when (= time-millis 1000)
      (setq time-integer (1+ time-integer))
      (setq time-millis 0))
    (multiple-value-bind
      (second minute hour date month year day-of-week dst-p tz)
      ;; Some Lisps allow TZ to be null but CLHS doesn't explicitly allow it,
      ;; so work around null TZ here.
      (if tz (decode-universal-time time-integer (- tz))
        (decode-universal-time time-integer))
      (declare (ignore day-of-week))
      ;; DECODE-UNIVERSAL-TIME might return a timezone offset
      ;; which is a multiple of 1/3600 but not 1/60.
      ;; We need a multiple of 1/60 because our formatted
      ;; timezone offset has only minutes and seconds.
      (if (/= (mod tz 1/60) 0)
        ($timedate time-integer (/ (round (- tz) 1/60) 60))
        (let ((tz-offset (if dst-p (- 1 tz) (- tz))))
          (multiple-value-bind
            (tz-hours tz-hour-fraction)
            (truncate tz-offset)
            (let
              ((tz-sign (if (<= 0 tz-offset) #\+ #\-)))
              (if (= time-millis 0)
                (format nil "~4,'0d-~2,'0d-~2,'0d ~2,'0d:~2,'0d:~2,'0d~a~2,'0d:~2,'0d"
                    year month date hour minute second tz-sign (abs tz-hours) (floor (* 60 (abs tz-hour-fraction))))
                (format nil "~4,'0d-~2,'0d-~2,'0d ~2,'0d:~2,'0d:~2,'0d.~3,'0d~a~2,'0d:~2,'0d"
                    year month date hour minute second time-millis tz-sign (abs tz-hours) (floor (* 60 (abs tz-hour-fraction))))))))))))

;; Parse date/time strings in these formats (and only these):
;;
;;   YYYY-MM-DD([ T]hh:mm:ss)?([,.]n+)?([+-]hh:mm)?
;;   YYYY-MM-DD([ T]hh:mm:ss)?([,.]n+)?([+-]hhmm)?
;;   YYYY-MM-DD([ T]hh:mm:ss)?([,.]n+)?([+-]hh)?
;;   YYYY-MM-DD([ T]hh:mm:ss)?([,.]n+)?[Z]?
;;
;; where (...)? indicates an optional group (occurs zero or one times)
;; ...+ indicates one or more instances of ...,
;; and [...] indicates literal character alternatives.
;;
;; Trailing unparsed stuff causes the parser to fail (return NIL).

;; Originally, these functions all looked like
;;
;; (defun match-date-yyyy-mm-dd (s)
;;   (pregexp:pregexp-match-positions
;;    '#.(pregexp:pregexp "^([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])")
;;    s))
;;
;; However, sbcl produces incorrect results for this.  For example,
;;
;; (match-date-yyyy-mm-dd "1900-01-01 16:00:00-08:00")
;;
;; returns ((0 . 10) (0 . 4) (8 . 10) NIL).  But the correct answer is
;; ((0 . 10) (0 . 4) (5 . 7) (8 . 10)).
;;
;; But if you replace the '#.(pregexp:pregexp ...) with
;; (pregexp:pregexp ...), sbcl works.  But then we end up compiling
;; the the regexp on every call.  So we use a closure so the regexp is
;; compiled only once.
(let ((pat (pregexp:pregexp "^([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])")))
  (defun match-date-yyyy-mm-dd (s)
    (pregexp:pregexp-match-positions
     pat
     s)))

(let ((pat (pregexp:pregexp "^[ T]([0-9][0-9]):([0-9][0-9]):([0-9][0-9])")))
  (defun match-time-hh-mm-ss (s)
    (pregexp:pregexp-match-positions
     pat
     s)))

(let ((pat (pregexp:pregexp "^[,.]([0-9][0-9]*)")))
  (defun match-fraction-nnn (s)
    (pregexp:pregexp-match-positions
     pat
     s)))

  
(let ((pat (pregexp:pregexp "^([+-])([0-9][0-9]):([0-9][0-9])$")))
  (defun match-tz-hh-mm (s)
    (pregexp:pregexp-match-positions
     pat
     s)))

(let ((pat (pregexp:pregexp "^([+-])([0-9][0-9])([0-9][0-9])$")))
  (defun match-tz-hhmm (s)
    (pregexp:pregexp-match-positions
     pat
     s)))

(let ((pat (pregexp:pregexp "^([+-])([0-9][0-9])$")))
  (defun match-tz-hh (s)
    (pregexp:pregexp-match-positions
     pat
     s)))

(let ((pat (pregexp:pregexp "^Z$")))
  (defun match-tz-Z (s)
    (pregexp:pregexp-match-positions
     pat
     s)))

(defmfun $parse_timedate (s)
  (setq s (string-trim '(#\Space #\Tab #\Newline #\Return) s))
  (let (matches
	year month day
	(hours 0) (minutes 0) (seconds 0)
	(seconds-fraction 0) seconds-fraction-numerator tz)
    (if (setq matches (match-date-yyyy-mm-dd s))
      (progn 
        (multiple-value-setq (year month day)
	  (pregexp-extract-groups-integers matches s))
        (setq s (subseq s (cdr (elt matches 0)))))
      (return-from $parse_timedate nil))
    (when (setq matches (match-time-hh-mm-ss s))
      (multiple-value-setq (hours minutes seconds)
	(pregexp-extract-groups-integers matches s))
      (setq s (subseq s (cdr (elt matches 0)))))
    (when (setq matches (match-fraction-nnn s))
      (multiple-value-setq (seconds-fraction-numerator)
	(pregexp-extract-groups-integers matches s))
      (let ((group1 (elt matches 1)))
        (setq seconds-fraction (div seconds-fraction-numerator (expt 10 (- (cdr group1) (car group1))))))
      (setq s (subseq s (cdr (elt matches 0)))))
    (cond
      ((setq matches (match-tz-hh-mm s))
       (multiple-value-bind (tz-sign tz-hours tz-minutes)
	   (pregexp-extract-groups-integers matches s)
         (setq tz (* tz-sign (+ tz-hours (/ tz-minutes 60))))))
      ((setq matches (match-tz-hhmm s))
       (multiple-value-bind (tz-sign tz-hours tz-minutes)
	   (pregexp-extract-groups-integers matches s)
         (setq tz (* tz-sign (+ tz-hours (/ tz-minutes 60))))))
      ((setq matches (match-tz-hh s))
       (multiple-value-bind (tz-sign tz-hours)
	   (pregexp-extract-groups-integers matches s)
         (setq tz (* tz-sign tz-hours))))
      ((setq matches (match-tz-Z s))
       (setq tz 0))
      (t
        (if (> (length s) 0)
          (return-from $parse_timedate nil))))

    (encode-time-with-all-parts year month day hours minutes seconds seconds-fraction (if tz (- tz)))))

(defun pregexp-extract-groups-integers (matches s)
  (values-list (mapcar #'parse-integer-or-sign
                       (mapcar #'(lambda (ab)
				   (subseq s (car ab) (cdr ab)))
                               (rest matches)))))

(defun parse-integer-or-sign (s)
  (cond
    ((string= s "+") 1)
    ((string= s "-") -1)
    (t (parse-integer s))))

; Clisp (2.49) / Windows does have a problem with dates before 1970-01-01,
; therefore add 400 years in that case and subtract 12622780800
; (= parse_timedate("2300-01-01Z") (Lisp starts with 1900-01-01) in timezone
; GMT) afterwards.
; see discussion on mailing list circa 2015-04-21: "parse_timedate error"
;
; Nota bene that this approach is correct only if the daylight saving time flag
; is the same for the given date and date + 400 years. That is true for
; dates before 1970-01-01 and after 2038-01-18, for Clisp at least,
; which ignores daylight saving time for all dates in those ranges,
; effectively making them all standard time.

#+(and clisp win32)
(defun encode-time-with-all-parts (year month day hours minutes seconds-integer seconds-fraction tz)
  ;; Experimenting with Clisp 2.49 for Windows seems to show that the bug
  ;; is triggered when local time zone is east of UTC, for times before
  ;; 1970-01-01 00:00:00 UTC + the number of hours of the time zone.
  ;; So apply the bug workaround to all times < 1970-01-02.
  (if (or (< year 1970) (and (= year 1970) (= day 1)))
    (sub (encode-time-with-all-parts (add year 400) month day hours minutes seconds-integer seconds-fraction tz) 12622780800)
    (add seconds-fraction
         ;; Some Lisps allow TZ to be null but CLHS doesn't explicitly allow it,
         ;; so work around null TZ here.
         (if tz
           (encode-universal-time seconds-integer minutes hours day month year tz)
           (encode-universal-time seconds-integer minutes hours day month year)))))

#-(and clisp win32)
(defun encode-time-with-all-parts (year month day hours minutes seconds-integer seconds-fraction tz)
  (add seconds-fraction
       ;; Some Lisps allow TZ to be null but CLHS doesn't explicitly allow it,
       ;; so work around null TZ here.
       (if tz
         (encode-universal-time seconds-integer minutes hours day month year tz)
         (encode-universal-time seconds-integer minutes hours day month year))))

(defmfun $encode_time (year month day hours minutes seconds &optional tz-offset)
    (when tz-offset
      (setq tz-offset (sub 0 tz-offset))
      (cond
        ((and (consp tz-offset) (eq (caar tz-offset) 'rat))
         (setq tz-offset (/ (second tz-offset) (third tz-offset))))
        ((floatp tz-offset)
         (setq tz-offset (rationalize tz-offset))))
      (setq tz-offset (/ (round tz-offset 1/3600) 3600)))
      (let*
        ((seconds-integer (mfuncall '$floor seconds))
         (seconds-fraction (sub seconds seconds-integer)))
        (encode-time-with-all-parts year month day hours minutes seconds-integer seconds-fraction tz-offset)))

(defmfun $decode_time (seconds &optional tz)
  (cond
    ((and (consp tz) (eq (caar tz) 'rat))
     (setq tz (/ (second tz) (third tz))))
    ((floatp tz)
     (setq tz (rationalize tz))))
  (if tz (setq tz (/ (round tz 1/3600) 3600)))
  (let*
    ((seconds-integer (mfuncall '$floor seconds))
     (seconds-fraction (sub seconds seconds-integer)))
    (multiple-value-bind
      (seconds minutes hours day month year day-of-week dst-p tz)
      ;; Some Lisps allow TZ to be null but CLHS doesn't explicitly allow it,
      ;; so work around null TZ here.
      (if tz (decode-universal-time seconds-integer (- tz))
          (decode-universal-time seconds-integer))
      (declare (ignore day-of-week))
      ;; HMM, CAN DECODE-UNIVERSAL-TIME RETURN TZ = NIL ??
      (let ((tz-offset (if dst-p (- 1 tz) (- tz))))
        (list '(mlist) year month day hours minutes (add seconds seconds-fraction) ($ratsimp tz-offset))))))

;;Some systems make everything functionp including macros:
(defun functionp (x)
  (cond ((symbolp x)
	 (and (not (macro-function x))
	      (fboundp x) t))
	 ((cl:functionp x))))

;; These symbols are shadowed because we use them also as special
;; variables.
(deff break #'cl:break)
(deff gcd #'cl:gcd)
