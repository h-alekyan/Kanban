function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ taskId: taskId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}
