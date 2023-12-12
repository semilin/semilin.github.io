(require 'ox-publish)

(setq org-html-validation-link nil	;; Don't show validation link
      org-html-head-include-scripts nil	;; Use our own scripts
      org-html-head-include-default-style nil ;; Use our own styles
      org-html-head "<link rel=\"stylesheet\" href=\"https://cdn.jsdelivr.net/gh/kimeiga/bahunya/dist/bahunya.min.css\">"
      org-html-preamble t
      org-html-preamble-format '(("en"
				  "<nav>
  <a href=\"/\">home</a>
  <a href=\"/blog/\">blog</a>
</nav>
<h1>%t</h1>
<p>%d</p>")))

;; Define the publishing project
(setq org-publish-project-alist
      (list
       (list "my-org-site"
             :recursive t
             :base-directory "./src"
             :publishing-directory "./docs"
             :publishing-function 'org-html-publish-to-html
	     :with-author nil
	     :with-title nil
	     :with-creator t
	     :with-toc t
	     :with-date t
	     :section-numbers nil
	     :time-stamp-file nil
	     :auto-preamble t
	     )))

(require 'org-id)
(setq org-id-link-to-org-use-id 'create-if-interactive-and-no-custom-id)

;; taken from https://writequit.org/articles/emacs-org-mode-generate-ids.html

(defun eos/org-custom-id-get (&optional pom create prefix)
  "Get the CUSTOM_ID property of the entry at point-or-marker POM.
   If POM is nil, refer to the entry at point. If the entry does
   not have an CUSTOM_ID, the function returns nil. However, when
   CREATE is non nil, create a CUSTOM_ID if none is present
   already. PREFIX will be passed through to `org-id-new'. In any
   case, the CUSTOM_ID of the entry is returned."
  (interactive)
  (org-with-point-at pom
    (let ((id (org-entry-get nil "CUSTOM_ID")))
      (cond
       ((and id (stringp id) (string-match "\\S-" id))
        id)
       (create
        (setq id (org-id-new (concat prefix "h")))
        (org-entry-put pom "CUSTOM_ID" id)
        (org-id-add-location id (buffer-file-name (buffer-base-buffer)))
        id)))))

(defun eos/org-add-ids-to-headlines-in-file ()
  "Add CUSTOM_ID properties to all headlines in the
   current file which do not already have one."
  (interactive)
  (org-map-entries (lambda () (eos/org-custom-id-get (point) 'create))))

;; Generate the site output
(org-publish-all t)

(message "Build complete!")
