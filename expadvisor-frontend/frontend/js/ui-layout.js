/**
 * ExpAdvisor Shared UI Layout & Navigation Helper
 * Handles active route navigation states, responsive sidebar drawer toggles, and shared modals.
 */

(function () {
    "use strict";

    function setActiveNavLinks() {
        const currentPath = window.location.pathname.split("/").pop() || "dashboard.html";
        const navLinks = document.querySelectorAll("nav a, aside a");

        navLinks.forEach((link) => {
            const href = link.getAttribute("href");
            if (!href) return;
            const targetPath = href.split("/").pop();

            if (targetPath === currentPath || (currentPath === "" && targetPath === "dashboard.html")) {
                link.classList.add("bg-brand-50", "text-brand-600", "font-semibold");
            }
        });
    }

    function initMobileSidebar() {
        const toggleButtons = document.querySelectorAll("[data-sidebar-toggle], #mobileSidebarToggle");
        const sidebar = document.querySelector("aside, #sidebarDrawer");
        const backdrop = document.querySelector("#sidebarBackdrop");

        if (!sidebar) return;

        function toggle() {
            sidebar.classList.toggle("-translate-x-full");
            sidebar.classList.toggle("translate-x-0");
            if (backdrop) {
                backdrop.classList.toggle("hidden");
            }
        }

        toggleButtons.forEach((btn) => btn.addEventListener("click", toggle));
        if (backdrop) backdrop.addEventListener("click", toggle);
    }

    function initNotificationsDropdown() {
        const notifBtn = document.querySelector("[data-notifications-toggle], #notificationsToggle");
        const notifMenu = document.querySelector("[data-notifications-menu], #notificationsMenu");

        if (notifBtn && notifMenu) {
            notifBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                notifMenu.classList.toggle("hidden");
            });

            document.addEventListener("click", (e) => {
                if (!notifMenu.contains(e.target) && !notifBtn.contains(e.target)) {
                    notifMenu.classList.add("hidden");
                }
            });
        }
    }

    function initUserDropdown() {
        const userBtn = document.querySelector("[data-user-menu-toggle], #userMenuToggle");
        const userMenu = document.querySelector("[data-user-menu], #userMenu");

        if (userBtn && userMenu) {
            userBtn.addEventListener("click", (e) => {
                e.stopPropagation();
                userMenu.classList.toggle("hidden");
            });

            document.addEventListener("click", (e) => {
                if (!userMenu.contains(e.target) && !userBtn.contains(e.target)) {
                    userMenu.classList.add("hidden");
                }
            });
        }
    }

    window.initAppLayout = function () {
        setActiveNavLinks();
        initMobileSidebar();
        initNotificationsDropdown();
        initUserDropdown();
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", window.initAppLayout);
    } else {
        window.initAppLayout();
    }
})();
