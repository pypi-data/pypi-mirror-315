;;; -*- Mode: Lisp; Package: Macsyma -*-                                 ;;;
;;;    (c) Copyright 1984 the Regents of the University of California.   ;;;
;;;        All Rights Reserved.                                          ;;;
;;;        This work was produced under the sponsorship of the           ;;;
;;;        U.S. Department of Energy.  The Government retains            ;;;
;;;        certain rights therein.                                       ;;;
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(macsyma-module rducon)

(eval-when
    (:load-toplevel :execute)
  (or (get 'expens 'version)
      ($load "expense")))

(defmvar $const_eqns (list '(mlist simp))
	 "List of equations of constant expressions found by REDUCE_CONSTS."
	 modified-commands '$reduce_consts)

(defmvar $const_prefix '$xx
	 "String used to prefix all symbols generated by REDUCE_CONSTS to
   represent constant expressions."
	 modified-commands '$reduce_consts)

(defmvar $const_counter 1
	 "Integer index used to uniquely identify all constant expressions
   found by calling REDUCE_CONSTS."
	 fixnum
	 modified-commands '$reduce_consts)

(defmacro minus-constantp (x)
  `(and (eq (caar ,x) 'mtimes)
	(= (length ,x) 3)
	(equal (cadr ,x) -1)))

(defun query-const-table (x)
   (do ((p (cdr $const_eqns) (cdr p)))
       ((null p))
     (and (alike1 (caddar p) x)
	  (return (cadar p)))))

(defun new-name (default-name)
   (let ((name (or default-name
		   (prog1
		    (implode (nconc (exploden $const_prefix)
				    (exploden $const_counter)))
		    (incf $const_counter)))))
     (MFUNCALL '$declare name '$constant)
     name))

(defun log-const (exp name)
   (let ((inconst (new-name name)))
     (setq $const_eqns `(,.$const_eqns ,`((mequal simp) ,inconst ,exp)))
     inconst))

(defun obtain-constant (key curr-const)
 (let ((inkey key))
   (or (query-const-table key)
       (do ((pursue (cdr $const_eqns) (cdr pursue))
	    (pointer)
	    (hold)
	    (op)
	    (expense ($expense key))
	    (negative (mul -1 key))
	    (sum? (mplusp key)))
	   ((null pursue)
	    (and pointer
		 (setq inkey
		       (cond ((eq op 'sum) (add (cadar pointer) hold))
			     ((eq op 'neg) (mul -1 (add (cadar pointer) hold)))
			     (t (mul (cadar pointer) hold))))
		 (do ((recheck (cdr $const_eqns) (cdr recheck))
		      (minkey (mul -1 inkey)))
		     ((null recheck))
		   (let ((exp (caddar recheck))
			 (lab (cadar recheck)))
		     (cond ((alike1 exp inkey) (return lab))
			   ((alike1 exp minkey)
			    (return (mul -1 lab))))))))
	 (let ((rhs (caddar pursue)))
	   (cond ((alike1 negative rhs) (return (mul -1 (cadar pursue))))
		 ((and sum?
		       (mplusp rhs)
		       (let ((trial (sub key rhs))
			     (trial-2 (sub negative rhs)))
			 (let ((estim (1+ ($expense trial)))
			       (estim-2 (1+ ($expense trial-2))))
			   (cond ((< estim estim-2)
				  (and (< estim expense)
				       (setq pointer pursue
					     op 'sum
					     expense estim
					     hold trial)))
				 (t
				  (and (< estim-2 expense)
				       (setq pointer pursue
					     op 'neg
					     expense estim-2
					     hold trial-2))))))))
		 (t
		  (let* ((trial (div key rhs))
			 (estim (1+ ($expense trial))))
		    (and (< estim expense)
			 (setq pointer pursue
			       op 'prod
			       expense estim
			       hold trial)))))))
       (log-const inkey curr-const))))

(defun find-constant (x)
   (cond ((and (symbolp x) ($constantp x)) x)
	 ((mtimesp x)
	  (do ((fcon x (cdr fcon)))
	      ((null (cdr fcon)))
	    (let ((qcon (cadr fcon)))
	      (and (symbolp qcon) ($constantp qcon) (return qcon)))))
	 (t nil)))

(defun reduce-constants (x &optional newconst)
   (cond ((or ($mapatom x)
	      (and (eq (caar x) 'mtimes)
		   (equal (cadr x) -1)
		   ($mapatom (caddr x))
		   (null (cdddr x))))
	  x)
	 ((query-const-table x))
	 ((and (eq (caar x) 'mexpt)
	       ($constantp x)
	       (let ((xexpon (caddr x)) (xbase (cadr x)))
		 (do ((p (cdr $const_eqns) (cdr p))
		      (nstate (integerp xexpon))
		      (follow $const_eqns p))
		     ((null p))
		   (let ((obj (caddar p)))
		     (and (mexptp obj)
			  (alike1 xbase (cadr obj))
			  (let ((inquir-expon (caddr obj)))
			    (let ((both-fix (and nstate (integerp inquir-expon))))
			      (let ((dif (cond (both-fix (- xexpon inquir-expon))
					       (t (sub xexpon inquir-expon))))
				    (gcd (cond (both-fix (gcd xexpon inquir-expon))
					       (t ($gcd xexpon inquir-expon)))))
				(or (and (integerp dif)
					 (cond ((equal 1 dif)
						(let ((new-exp (mul (cadar p) xbase)))
						  (return (or (query-const-table new-exp)
							      (log-const new-exp newconst)))))
					       ((equal -1 dif)
						(let ((inc (new-name newconst)))
						  (rplaca (cddar p) (mul inc xbase))
						  (rplacd follow (append `(((mequal simp) ,inc ,x)) p))
						  (return inc)))))
				    (or (and (integerp gcd) (equal gcd 1))
					(let ((pw1 (cond (both-fix (quotient xexpon gcd))
							 (t (div xexpon gcd))))
					      (pw2 (cond (both-fix (quotient inquir-expon gcd))
							 (t (div inquir-expon gcd)))))
					  (cond ((and (integerp pw2) (equal pw2 1))
						 (let ((new-exp (power (cadar p) pw1)))
						   (return (or (query-const-table new-exp)
							       (log-const new-exp newconst)))))
						((and (integerp pw1) (equal pw1 1))
						 (let ((inc (new-name newconst)))
						   (rplaca (cddar p) (power inc pw2))
						   (rplacd follow (append `(((mequal simp) ,inc ,x)) p))
						   (return inc)))
						(t (let ((inc (new-name nil)))
						     (rplaca (cddar p) (power inc pw2))
						     (rplacd follow (append `(((mequal simp) ,inc ,(power xbase gcd))) p))
						     (return (log-const (power inc pw1) newconst)))))))))))))))))
	 (($constantp x) (obtain-constant x newconst))
	 (t
	  (let ((opr (caar x)))
	    (cond ((member opr '(mtimes mplus) :test #'eq)
		   (let* ((product (eq opr 'mtimes))
			  (negative (and product (equal (cadr x) -1))))
		     (or (and negative (null (cdddr x))
			      (let ((new? (query-const-table (caddr x))))
				(and new? (mul -1 new?))))
			 (do ((next (cdr x) (cdr next))
			      (itot 0)
			      (new)
			      (non-constants))
			     ((null next)
			      (cond ((and product (= (length new) 2) (equal (car new) -1))
				     (muln (nconc new non-constants) nil))
				    ((> (length new) 1)
				     (let ((nc (obtain-constant (cond (product (muln new nil))
								      (t (addn new nil)))
								newconst)))
				       (cond ((not product) (addn `(,.non-constants ,nc) nil))
					     ((atom nc) (muln `(,.non-constants ,nc) nil))
					     (t (muln (nconc (cdr nc) non-constants) nil)))))
				    ((or new non-constants)
				     (let ((tot (nconc new non-constants)))
				       (cond (product (muln tot nil))
					     (t (addn tot nil)))))
				    (t x)))
			   (declare (fixnum itot))
			   (let* ((exam (car next))
				  (result (reduce-constants exam)))
			     (cond ((eq exam result)
				    (cond (($constantp exam)
					   (incf itot)
					   (if (and (null new)
						    (cond (negative (> itot 2))
							  (t (> itot 1))))
					       (do ((seplist (cdr x) (cdr seplist)))
						   ((eq seplist next))
						 (let ((element (car seplist)))
						   (cond (($constantp element)
							  (setq new `(,.new ,element)))
							 (t (setq non-constants `(,.non-constants ,element)))))))
					   (and new (setq new `(,.new ,exam))))
					  ((or new non-constants) (setq non-constants `(,.non-constants ,exam)))))
				   (t
				    (or new non-constants
					(do ((seplist (cdr x) (cdr seplist)))
					    ((eq seplist next))
					  (let ((element (car seplist)))
					    (cond (($constantp element)
						   (setq new `(,.new ,element)))
						  (t (setq non-constants `(,.non-constants ,element)))))))
				    (cond ((or (atom result) (minus-constantp result))
					   (setq new
						 (cond ((or (atom result) (not product)) `(,.new ,result))
						       (t
							(let ((number? (car new)))
							  (cond (($numberp number?)
								 (let ((new-prod (mul number? result)))
								   (cond ((mtimesp new-prod)
									  (nconc (cdr new-prod) (ncons new-prod)))
									 (t (nconc (cdr new) (ncons new-prod))))))
								(t (nconc (cdr result) new))))))))
					  (t (setq non-constants `(,.non-constants ,result)))))))))))
		  (t
		   (do ((next (cdr x) (cdr next))
			(new))
		       ((null next)
			(cond ((null new) x)
			      ((not (eq opr 'mquotient))
			       (nconc (ncons (car x)) new))
			      (t
			       (let ((cnum (find-constant (car new)))
				     (cden (find-constant (cadr new))))
				 (cond ((and cnum cden)
					(let* ((ratio (obtain-constant (div cnum cden) newconst))
					       (numerator (cond ((mtimesp (car new))
								 (mul ratio (remove cnum (car new) :test #'eq)))
								(t ratio))))
					  (cond ((mtimesp (cadr new))
						 (div numerator (muln (remove cden (cdadr new) :test #'eq) nil)))
						(t numerator))))
				       (t x))))))
		     (let* ((exam (car next))
			    (result (reduce-constants exam)))
		       (cond ((eq exam result)
			      (and new (setq new `(,.new ,exam))))
			     (t
			      (or new
				  (do ((copy (cdr x) (cdr copy)))
				      ((eq copy next))
				    (setq new `(,.new ,(car copy)))))
			      (setq new `(,.new ,result))))))))))))

(defun $reduce_consts (x &optional newconstant)
   (cond ((atom x) x)
	 (t (reduce-constants x newconstant))))
