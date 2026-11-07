// First Will & Estate Basics Guide — checklist persistence.
// Local-first: progress is stored in this browser's localStorage only.
// No network calls, no analytics, no external resources.
(function () {
  "use strict";

  var STORAGE_KEY = "estate-basics-checklist-v1";

  function loadState() {
    try {
      var raw = window.localStorage.getItem(STORAGE_KEY);
      if (!raw) return {};
      var parsed = JSON.parse(raw);
      return parsed && typeof parsed === "object" ? parsed : {};
    } catch (err) {
      return {};
    }
  }

  function saveState(state) {
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (err) {
      // Storage may be unavailable (private mode, etc). Checkboxes still work
      // for the session; persistence is best-effort by design.
    }
  }

  // Deterministic per-checkbox id: phase number + label text, so stored
  // progress survives harmless text edits and stays stable across revisits.
  function checkboxKey(phase, index, labelText) {
    var slug = labelText
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, "-")
      .slice(0, 60);
    return "p" + phase + "-" + index + "-" + slug;
  }

  function init() {
    var lists = document.querySelectorAll(".checklist");
    if (lists.length === 0) return;

    var state = loadState();

    lists.forEach(function (list) {
      var phase = list.getAttribute("data-phase") || "0";
      var items = list.querySelectorAll('input[type="checkbox"]');
      items.forEach(function (box, index) {
        var label = box.closest("label");
        var text = label ? label.textContent.trim() : String(index);
        var key = checkboxKey(phase, index, text);

        if (state[key] === true) {
          box.checked = true;
        }

        function refresh() {
          if (label) {
            label.parentElement.classList.toggle("done", box.checked);
          }
          state[key] = box.checked;
          saveState(state);
        }

        box.addEventListener("change", refresh);
        refresh();
      });
    });

    var reset = document.getElementById("reset-progress");
    if (reset) {
      reset.addEventListener("click", function () {
        var confirmed = window.confirm(
          "Clear all saved checklist progress? (Stored only in this browser.)"
        );
        if (!confirmed) return;
        try {
          window.localStorage.removeItem(STORAGE_KEY);
        } catch (err) {
          // ignore
        }
        lists.forEach(function (list) {
          list.querySelectorAll('input[type="checkbox"]').forEach(function (box) {
            box.checked = false;
            var label = box.closest("label");
            if (label && label.parentElement) {
              label.parentElement.classList.remove("done");
            }
          });
        });
      });
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
