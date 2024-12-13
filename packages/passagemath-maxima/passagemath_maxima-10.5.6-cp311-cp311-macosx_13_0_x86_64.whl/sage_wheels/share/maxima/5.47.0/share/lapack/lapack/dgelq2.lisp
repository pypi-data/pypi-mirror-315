;;; Compiled by f2cl version:
;;; ("f2cl1.l,v 2edcbd958861 2012/05/30 03:34:52 toy $"
;;;  "f2cl2.l,v 96616d88fb7e 2008/02/22 22:19:34 rtoy $"
;;;  "f2cl3.l,v 96616d88fb7e 2008/02/22 22:19:34 rtoy $"
;;;  "f2cl4.l,v 96616d88fb7e 2008/02/22 22:19:34 rtoy $"
;;;  "f2cl5.l,v 3fe93de3be82 2012/05/06 02:17:14 toy $"
;;;  "f2cl6.l,v 1d5cbacbb977 2008/08/24 00:56:27 rtoy $"
;;;  "macros.l,v 3fe93de3be82 2012/05/06 02:17:14 toy $")

;;; Using Lisp CMU Common Lisp 20d (20D Unicode)
;;; 
;;; Options: ((:prune-labels nil) (:auto-save t) (:relaxed-array-decls t)
;;;           (:coerce-assigns :as-needed) (:array-type ':array)
;;;           (:array-slicing t) (:declare-common nil)
;;;           (:float-format double-float))

(in-package :lapack)


(let* ((one 1.0))
  (declare (type (double-float 1.0 1.0) one) (ignorable one))
  (defun dgelq2 (m n a lda tau work info)
    (declare (type (array double-float (*)) work tau a)
             (type (f2cl-lib:integer4) info lda n m))
    (f2cl-lib:with-multi-array-data
        ((a double-float a-%data% a-%offset%)
         (tau double-float tau-%data% tau-%offset%)
         (work double-float work-%data% work-%offset%))
      (prog ((aii 0.0) (i 0) (k 0))
        (declare (type (double-float) aii) (type (f2cl-lib:integer4) i k))
        (setf info 0)
        (cond
          ((< m 0)
           (setf info -1))
          ((< n 0)
           (setf info -2))
          ((< lda (max (the f2cl-lib:integer4 1) (the f2cl-lib:integer4 m)))
           (setf info -4)))
        (cond
          ((/= info 0)
           (xerbla "DGELQ2" (f2cl-lib:int-sub info))
           (go end_label)))
        (setf k (min (the f2cl-lib:integer4 m) (the f2cl-lib:integer4 n)))
        (f2cl-lib:fdo (i 1 (f2cl-lib:int-add i 1))
                      ((> i k) nil)
          (tagbody
            (multiple-value-bind (var-0 var-1 var-2 var-3 var-4)
                (dlarfg (f2cl-lib:int-add (f2cl-lib:int-sub n i) 1)
                 (f2cl-lib:fref a-%data% (i i) ((1 lda) (1 *)) a-%offset%)
                 (f2cl-lib:array-slice a-%data%
                                       double-float
                                       (i
                                        (min
                                         (the f2cl-lib:integer4
                                              (f2cl-lib:int-add i 1))
                                         (the f2cl-lib:integer4 n)))
                                       ((1 lda) (1 *))
                                       a-%offset%)
                 lda (f2cl-lib:fref tau-%data% (i) ((1 *)) tau-%offset%))
              (declare (ignore var-0 var-2 var-3))
              (setf (f2cl-lib:fref a-%data% (i i) ((1 lda) (1 *)) a-%offset%)
                      var-1)
              (setf (f2cl-lib:fref tau-%data% (i) ((1 *)) tau-%offset%) var-4))
            (cond
              ((< i m)
               (setf aii
                       (f2cl-lib:fref a-%data%
                                      (i i)
                                      ((1 lda) (1 *))
                                      a-%offset%))
               (setf (f2cl-lib:fref a-%data% (i i) ((1 lda) (1 *)) a-%offset%)
                       one)
               (dlarf "Right" (f2cl-lib:int-sub m i)
                (f2cl-lib:int-add (f2cl-lib:int-sub n i) 1)
                (f2cl-lib:array-slice a-%data%
                                      double-float
                                      (i i)
                                      ((1 lda) (1 *))
                                      a-%offset%)
                lda (f2cl-lib:fref tau-%data% (i) ((1 *)) tau-%offset%)
                (f2cl-lib:array-slice a-%data%
                                      double-float
                                      ((+ i 1) i)
                                      ((1 lda) (1 *))
                                      a-%offset%)
                lda work)
               (setf (f2cl-lib:fref a-%data% (i i) ((1 lda) (1 *)) a-%offset%)
                       aii)))
           label10))
        (go end_label)
       end_label
        (return (values nil nil nil nil nil nil info))))))

(in-package #:cl-user)
#+#.(cl:if (cl:find-package '#:f2cl) '(and) '(or))
(eval-when (:load-toplevel :compile-toplevel :execute)
  (setf (gethash 'fortran-to-lisp::dgelq2
                 fortran-to-lisp::*f2cl-function-info*)
          (fortran-to-lisp::make-f2cl-finfo
           :arg-types '((fortran-to-lisp::integer4) (fortran-to-lisp::integer4)
                        (array double-float (*)) (fortran-to-lisp::integer4)
                        (array double-float (*)) (array double-float (*))
                        (fortran-to-lisp::integer4))
           :return-values '(nil nil nil nil nil nil fortran-to-lisp::info)
           :calls '(fortran-to-lisp::dlarf fortran-to-lisp::dlarfg
                    fortran-to-lisp::xerbla))))

