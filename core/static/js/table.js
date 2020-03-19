$(document).ready(function() {
    $('#dasbord').DataTable({
        "language": {
    "emptyTable":     "Нет данных в таблице",
    "info":           "Показанны с _START_ до  _END_ из _TOTAL_",
    "infoEmpty":      "Показанны от 0 до 0 из 0 ",
    "infoFiltered":   "(filtered from _MAX_ total entries)",
    "infoPostFix":    "",
    "thousands":      ",",
    "lengthMenu":     "Показать _MENU_ ",
    "loadingRecords": "Загрузка...",
    "processing":     "Processing...",
    "search":         "Поиск:",
    "zeroRecords":    "Не найденно записей",
    "paginate": {
        "first":      "Первый",
        "last":       "Последний",
        "next":       "Следующий",
        "previous":   "Предыдущий"
    }
    }
    });
} );
