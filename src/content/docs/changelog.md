---
title: 更新日志
---
`LOG`
#### v0.1.1 (<span class='log-date' data-time='2026-04-26T07:46:17.243095+00:00'>2026-04-26 07:46 UTC</span>)

* 更改了更新日志页面的显示时间为动态显示当地UTC时间。

---


#### v0.1.0 (2026-04-26 07:28)

* 新增合祀星生活习俗词条，涵盖饮食、服饰、居住、节律、节日与娱乐。

---


<script>
  function convertToLocalTime() {
    const dateElements = document.querySelectorAll('.log-date');
    dateElements.forEach(el => {
      const utcTime = el.getAttribute('data-time');
      if (utcTime) {
        const localDate = new Date(utcTime);
        el.innerText = localDate.toLocaleString(undefined, {
          year: 'numeric',
          month: 'numeric',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          hour12: false
        });
      }
    });
  }
  convertToLocalTime();
  window.addEventListener('astro:page-load', convertToLocalTime);
</script>
