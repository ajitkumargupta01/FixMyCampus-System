// Main JavaScript file for FixMyCampus

// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Password confirmation validation
    const newPasswordInput = document.getElementById('new_password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const passwordMatchError = document.getElementById('password-match-error');
    const passwordForm = document.getElementById('change-password-form');
    
    if (confirmPasswordInput && newPasswordInput && passwordForm) {
        // Check if passwords match
        function checkPasswordMatch() {
            if (confirmPasswordInput.value && confirmPasswordInput.value !== newPasswordInput.value) {
                passwordMatchError.classList.remove('hidden');
                return false;
            } else {
                passwordMatchError.classList.add('hidden');
                return true;
            }
        }
        
        confirmPasswordInput.addEventListener('input', checkPasswordMatch);
        newPasswordInput.addEventListener('input', function() {
            if (confirmPasswordInput.value) {
                checkPasswordMatch();
            }
        });
        
        // Validate form before submission
        passwordForm.addEventListener('submit', function(e) {
            if (!checkPasswordMatch()) {
                e.preventDefault();
            }
        });
    }

    // FAQ accordion functionality
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    if (faqQuestions.length > 0) {
        faqQuestions.forEach(question => {
            question.addEventListener('click', function() {
                const answer = this.nextElementSibling;
                const icon = this.querySelector('.question-icon');
                
                // Close all other answers
                document.querySelectorAll('.faq-answer').forEach(item => {
                    if (item !== answer) {
                        item.classList.add('hidden');
                        const otherIcon = item.previousElementSibling.querySelector('.question-icon');
                        if (otherIcon) {
                            otherIcon.classList.remove('rotate-90');
                        }
                    }
                });
                
                // Toggle current answer
                answer.classList.toggle('hidden');
                if (icon) {
                    icon.classList.toggle('rotate-90');
                }
            });
        });
    }

    // Issue filtering functionality
    const statusFilter = document.getElementById('filter-status');
    const categoryFilter = document.getElementById('filter-category');
    const sortBy = document.getElementById('sort-by');
    const resetButton = document.getElementById('reset-filters');
    const issueItems = document.querySelectorAll('.issue-item');
    
    if (statusFilter && categoryFilter && sortBy && resetButton && issueItems.length > 0) {
        function applyFilters() {
            const selectedStatus = statusFilter.value;
            const selectedCategory = categoryFilter.value;
            const selectedSort = sortBy.value;
            
            // Convert issue items to array for sorting
            const issuesArray = Array.from(issueItems);
            
            // Sort issues
            issuesArray.sort(function(a, b) {
                const dateA = new Date(a.dataset.date);
                const dateB = new Date(b.dataset.date);
                
                if (selectedSort === 'newest') {
                    return dateB - dateA;
                } else {
                    return dateA - dateB;
                }
            });
            
            // Filter and display issues
            issuesArray.forEach(function(item) {
                const itemStatus = item.dataset.status;
                const itemCategory = item.dataset.category;
                
                const statusMatch = selectedStatus === 'all' || itemStatus === selectedStatus;
                const categoryMatch = selectedCategory === 'all' || itemCategory === selectedCategory;
                
                if (statusMatch && categoryMatch) {
                    item.style.display = 'block';
                } else {
                    item.style.display = 'none';
                }
            });
            
            // Reattach sorted and filtered elements
            const issueList = document.querySelector('.issue-list');
            if (issueList) {
                issuesArray.forEach(function(item) {
                    issueList.appendChild(item);
                });
            }
        }
        
        statusFilter.addEventListener('change', applyFilters);
        categoryFilter.addEventListener('change', applyFilters);
        sortBy.addEventListener('change', applyFilters);
        
        resetButton.addEventListener('click', function() {
            statusFilter.value = 'all';
            categoryFilter.value = 'all';
            sortBy.value = 'newest';
            applyFilters();
        });
        
        // Initial sort (newest first by default)
        applyFilters();
    }

    // Profile edit modal functionality
    const editProfileBtn = document.getElementById('edit-profile-btn');
    const editProfileModal = document.getElementById('edit-profile-modal');
    const closeModalBtn = document.getElementById('close-modal');
    const cancelEditBtn = document.getElementById('cancel-edit');
    
    if (editProfileBtn && editProfileModal && closeModalBtn && cancelEditBtn) {
        function openModal() {
            editProfileModal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
        
        function closeModal() {
            editProfileModal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
        
        editProfileBtn.addEventListener('click', openModal);
        closeModalBtn.addEventListener('click', closeModal);
        cancelEditBtn.addEventListener('click', closeModal);
        
        // Close modal when clicking outside
        editProfileModal.addEventListener('click', function(e) {
            if (e.target === editProfileModal) {
                closeModal();
            }
        });
    }

    // Custom issue type toggle
    const issueTypeSelect = document.getElementById('issue_type');
    const otherIssueContainer = document.getElementById('other_issue_container');
    const customIssueInput = document.getElementById('custom_issue_type');
    
    if (issueTypeSelect && otherIssueContainer && customIssueInput) {
        // Show/hide the custom issue type input based on selection
        issueTypeSelect.addEventListener('change', function() {
            if (this.value === 'Other') {
                otherIssueContainer.classList.remove('hidden');
                customIssueInput.setAttribute('required', 'required');
            } else {
                otherIssueContainer.classList.add('hidden');
                customIssueInput.removeAttribute('required');
            }
        });
    }
});