(load "~/.config/emacs/straight/build/htmlize/htmlize")

;; Load the publishing system
(require 'ox-publish)

(setq org-html-validation-link nil
      org-html-head-include-scripts nil
      org-html-head-include-default-style nil
      org-html-head "<link rel=\"stylesheet\" href=\"../style.css\"/>")

(setq org-publish-project-alist
      (list
       (list "my-org-site"
	     :recursive t
	     :base-directory "./content"
	     :publishing-directory "./docs"
	     :publishing-function 'org-html-publish-to-html
	     :preamble "<header><nav><a href=\"/\">Home</a></nav></header>"
	     :with-author nil
	     :with-creator t
	     :with-toc t
	     :section-numbers nil
	     :time-stamp-file nil)))

;; Generate the site output
(org-publish-all t)

(message "Build complete!")
