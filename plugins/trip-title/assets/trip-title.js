require(["gitbook", "jquery"], function (gitbook, $) {
  function markEmptySection(section) {
    if (!section) {
      return;
    }

    if (section.children.length === 0 && section.textContent.trim() === "") {
      section.classList.add("is-empty-standalone");
    } else {
      section.classList.remove("is-empty-standalone");
    }
  }

  function placeStandaloneBlocks() {
    $(".markdown-section > .trip-title, .markdown-section > .trip-start, .markdown-section > .trip-loading-page").each(function () {
      var block = this;
      var section = block.parentNode;
      if (!section || !section.parentNode) {
        return;
      }

      block.classList.add("trip-standalone-block");
      section.parentNode.insertBefore(block, section);
      markEmptySection(section);
    });
  }

  function updateFullscreenMode() {
    var isFullscreen = $(".trip-start, .trip-loading-page").length > 0;

    $(".book").toggleClass("trip-fullscreen-mode", isFullscreen);
    $("body").toggleClass("trip-fullscreen-body", isFullscreen);
  }

  function hideUtilityPagesInSummary() {
    $(".book-summary li[data-path='loading.html']").hide();
  }

  function playPageReveal() {
    if (!window.sessionStorage || sessionStorage.getItem("trip-page-reveal") !== "true") {
      return;
    }

    sessionStorage.removeItem("trip-page-reveal");

    var mask = document.createElement("div");
    mask.className = "trip-page-reveal";
    document.body.appendChild(mask);

    window.requestAnimationFrame(function () {
      mask.classList.add("is-active");
    });

    window.setTimeout(function () {
      mask.remove();
    }, 940);
  }

  function scheduleLoadingRedirect() {
    var loading = document.querySelector(".trip-loading-page");
    if (!loading || loading.getAttribute("data-redirect-started") === "true") {
      return;
    }

    var params = new URLSearchParams(window.location.search);
    var next = params.get("to") || loading.getAttribute("data-next") || "overview.html";
    var delay = parseInt(loading.getAttribute("data-delay"), 10) || 2600;

    loading.setAttribute("data-redirect-started", "true");
    window.setTimeout(function () {
      if (window.sessionStorage) {
        sessionStorage.setItem("trip-page-reveal", "true");
      }

      window.location.href = next;
    }, delay);
  }

  function runTypewriters() {
    $("[data-typewriter]").each(function () {
      var el = this;
      var text = el.getAttribute("data-typewriter") || "";
      var delay = parseInt(el.getAttribute("data-typewriter-delay"), 10) || 30;
      var startTime = 0;

      if (!text || el.getAttribute("data-typewriter-started") === "true") {
        return;
      }

      el.setAttribute("data-typewriter-started", "true");
      el.setAttribute("aria-label", text);
      el.textContent = "";
      el.classList.add("is-typing");
      el.classList.remove("is-complete");

      function typeNext() {
        var elapsed = Date.now() - startTime;
        var index = Math.min(text.length, Math.max(1, Math.floor(elapsed / delay)));

        el.textContent = text.slice(0, index);
        if (index < text.length) {
          window.setTimeout(typeNext, Math.min(delay, 24));
        } else {
          el.classList.remove("is-typing");
          el.classList.add("is-complete");
        }
      }

      window.setTimeout(function () {
        startTime = Date.now();
        typeNext();
      }, 180);
    });
  }

  function updateTripTitle() {
    placeStandaloneBlocks();
    updateFullscreenMode();
    hideUtilityPagesInSummary();
    runTypewriters();
    playPageReveal();
    scheduleLoadingRedirect();
  }

  gitbook.events.on("page.change", updateTripTitle);
  $(updateTripTitle);
});
