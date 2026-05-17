document.addEventListener('DOMContentLoaded', () => {
  const sidebar = document.getElementById('appSidebar');
  const backdrop = document.getElementById('sidebarBackdrop');
  if (!sidebar || !backdrop) return;

  sidebar.addEventListener('show.bs.collapse', () => backdrop.classList.remove('d-none'));
  sidebar.addEventListener('hide.bs.collapse', () => backdrop.classList.add('d-none'));
  backdrop.addEventListener('click', () => {
    const collapse = bootstrap.Collapse.getOrCreateInstance(sidebar);
    collapse.hide();
  });
});
