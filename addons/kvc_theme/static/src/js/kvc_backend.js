/** @odoo-module **/
/**
 * KVC Backend JS — Odoo 18 Web Client enhancements
 * KaliVibeCoding Neon-Noir Design System
 */

import { patch } from "@web/core/utils/patch";
import { onMounted } from "@odoo/owl";

// ── Inject Google Fonts early ─────────────────────────────────
(function injectKvcFonts() {
    if (document.getElementById("kvc-fonts")) return;
    const link = document.createElement("link");
    link.id = "kvc-fonts";
    link.rel = "stylesheet";
    link.href =
        "https://fonts.googleapis.com/css2?family=Lobster&family=Montserrat:wght@400;500;600;700;800;900&family=Fira+Code:wght@400;500;600&display=swap";
    document.head.appendChild(link);
})();

// ── KVC brand badge in top navbar ─────────────────────────────
(function injectKvcBadge() {
    const tryInject = () => {
        const navbar = document.querySelector(".o_menu_brand, .o_navbar .o_menu_sections");
        if (!navbar) return;
        if (document.getElementById("kvc-brand-badge")) return;

        const badge = document.createElement("span");
        badge.id = "kvc-brand-badge";
        badge.innerHTML = "&#x25CF; KVC CRM";
        badge.style.cssText = `
            font-family: "Montserrat", sans-serif;
            font-size: 10px;
            font-weight: 700;
            color: rgba(255, 105, 180, 0.7);
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-left: 12px;
            vertical-align: middle;
        `;
        navbar.parentElement?.appendChild(badge);
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", tryInject);
    } else {
        // Retry since Odoo SPA loads async
        setTimeout(tryInject, 500);
        setTimeout(tryInject, 1500);
    }
})();

// ── Progress bar enhancement for kvc.student list view ────────
(function enhanceProgressBars() {
    const observer = new MutationObserver(() => {
        document.querySelectorAll(".o_field_progressbar").forEach((el) => {
            if (el.dataset.kvcStyled) return;
            el.dataset.kvcStyled = "1";

            const bar = el.querySelector(".o_progress_bar");
            if (bar) {
                bar.style.background = "linear-gradient(90deg, #ff69b4, #87ceeb)";
                bar.style.borderRadius = "999px";
            }

            const track = el.querySelector(".o_progressbar_value");
            if (track) {
                track.style.background = "rgba(240,240,240,0.08)";
                track.style.borderRadius = "999px";
            }
        });
    });

    observer.observe(document.body, { childList: true, subtree: true });
})();

// ── Kanban card stage glow on hover ───────────────────────────
(function enhanceKanbanCards() {
    document.addEventListener("mouseover", (e) => {
        const card = e.target.closest?.(".o_kanban_card");
        if (card && !card.dataset.kvcHoverWired) {
            card.dataset.kvcHoverWired = "1";
            card.addEventListener("mouseenter", () => {
                card.style.boxShadow =
                    "0 0 0 1px rgba(255,105,180,0.25), 0 4px 24px rgba(0,0,0,0.35)";
            });
            card.addEventListener("mouseleave", () => {
                card.style.boxShadow = "";
            });
        }
    });
})();

// ── Console watermark ─────────────────────────────────────────
console.log(
    "%cKVC CRM — KaliVibeCoding\n%cOdoo 18 · Neon-Noir · kalivibecoding.com",
    "color:#ff69b4;font-family:Lobster,cursive;font-size:18px;font-weight:bold;",
    "color:#9ca3af;font-size:11px;"
);
