// Reusable component functionality
class ComponentManager {
    constructor() {
        this.init();
    }

    init() {
        this.initModals();
        this.initDropdowns();
        this.initTabs();
        this.initAccordions();
    }

    // Modal functionality
    initModals() {
        const modalTriggers = document.querySelectorAll('[data-modal-target]');
        const modals = document.querySelectorAll('.modal');
        
        modalTriggers.forEach(trigger => {
            trigger.addEventListener('click', (e) => {
                e.preventDefault();
                const targetModal = document.getElementById(trigger.dataset.modalTarget);
                if (targetModal) {
                    this.openModal(targetModal);
                }
            });
        });

        modals.forEach(modal => {
            const closeButtons = modal.querySelectorAll('[data-modal-close]');
            closeButtons.forEach(btn => {
                btn.addEventListener('click', () => this.closeModal(modal));
            });

            modal.addEventListener('click', (e) => {
                if (e.target === modal) {
                    this.closeModal(modal);
                }
            });
        });

        // Close modals with Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                const openModal = document.querySelector('.modal.active');
                if (openModal) {
                    this.closeModal(openModal);
                }
            }
        });
    }

    openModal(modal) {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    closeModal(modal) {
        modal.classList.remove('active');
        document.body.style.overflow = '';
    }

    // Dropdown functionality
    initDropdowns() {
        const dropdowns = document.querySelectorAll('.dropdown');
        
        dropdowns.forEach(dropdown => {
            const trigger = dropdown.querySelector('.dropdown-trigger');
            const menu = dropdown.querySelector('.dropdown-menu');
            
            if (trigger && menu) {
                trigger.addEventListener('click', (e) => {
                    e.stopPropagation();
                    dropdown.classList.toggle('active');
                });
            }
        });

        // Close dropdowns when clicking outside
        document.addEventListener('click', () => {
            dropdowns.forEach(dropdown => {
                dropdown.classList.remove('active');
            });
        });
    }

    // Tab functionality
    initTabs() {
        const tabContainers = document.querySelectorAll('.tabs');
        
        tabContainers.forEach(container => {
            const tabButtons = container.querySelectorAll('.tab-button');
            const tabPanels = container.querySelectorAll('.tab-panel');
            
            tabButtons.forEach((button, index) => {
                button.addEventListener('click', () => {
                    // Remove active class from all tabs and panels
                    tabButtons.forEach(btn => btn.classList.remove('active'));
                    tabPanels.forEach(panel => panel.classList.remove('active'));
                    
                    // Add active class to clicked tab and corresponding panel
                    button.classList.add('active');
                    if (tabPanels[index]) {
                        tabPanels[index].classList.add('active');
                    }
                });
            });
        });
    }

    // Accordion functionality
    initAccordions() {
        const accordions = document.querySelectorAll('.accordion');
        
        accordions.forEach(accordion => {
            const items = accordion.querySelectorAll('.accordion-item');
            
            items.forEach(item => {
                const header = item.querySelector('.accordion-header');
                const content = item.querySelector('.accordion-content');
                
                if (header && content) {
                    header.addEventListener('click', () => {
                        const isActive = item.classList.contains('active');
                        
                        // Close all accordion items
                        items.forEach(otherItem => {
                            otherItem.classList.remove('active');
                        });
                        
                        // Open clicked item if it wasn't active
                        if (!isActive) {
                            item.classList.add('active');
                        }
                    });
                }
            });
        });
    }

    // Notification system
    showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <i class="fas fa-${this.getNotificationIcon(type)}"></i>
                <span>${message}</span>
            </div>
            <button class="notification-close">
                <i class="fas fa-times"></i>
            </button>
        `;

        // Add to notification container or body
        const container = document.querySelector('.notification-container') || document.body;
        container.appendChild(notification);

        // Close button functionality
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            this.removeNotification(notification);
        });

        // Auto remove after duration
        setTimeout(() => {
            this.removeNotification(notification);
        }, duration);

        return notification;
    }

    removeNotification(notification) {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(100%)';
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }

    getNotificationIcon(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-circle',
            warning: 'exclamation-triangle',
            info: 'info-circle'
        };
        return icons[type] || icons.info;
    }

    // Loading states
    setLoadingState(element, isLoading) {
        if (isLoading) {
            element.disabled = true;
            element.classList.add('loading');
            const originalContent = element.innerHTML;
            element.dataset.originalContent = originalContent;
            element.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        } else {
            element.disabled = false;
            element.classList.remove('loading');
            if (element.dataset.originalContent) {
                element.innerHTML = element.dataset.originalContent;
                delete element.dataset.originalContent;
            }
        }
    }
}

// Initialize component manager
const componentManager = new ComponentManager();

// Export for global access
window.componentManager = componentManager;
