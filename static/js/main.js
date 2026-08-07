function refreshKunci(labId) {
    var $kunci = $('#id_kunci');
    if (!$kunci.length) return;
    $kunci.empty();
    $kunci.prop('disabled', !labId);
    if (labId) {
        $kunci.append('<option value="">-- Pilih Kunci --</option>');
        $.getJSON('/transaksi/api/get-kunci/', { lab_id: labId }, function(data) {
            $.each(data.results, function(i, item) {
                $kunci.append('<option value="' + item.id + '">' + item.text + '</option>');
            });
        });
    } else {
        $kunci.append('<option value="">-- Pilih ruangan terlebih dahulu --</option>');
    }
}

function inisialisasiFormPeminjaman() {
    if (document.getElementById('form-peminjaman')) {
        refreshKunci($('#id_laboratorium').val());
    }
}

$(document).ready(function() {
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);

    // Jalankan sekali saat halaman full-load
    inisialisasiFormPeminjaman();

    // Delegasi: tetap berlaku meski konten di-swap htmx
    $(document).on('change', '#id_laboratorium', function() {
        refreshKunci($(this).val());
    });
});

// Jalankan ulang setelah setiap swap htmx (konten #main-content diperbarui)
document.addEventListener('htmx:afterSwap', function() {
    inisialisasiFormPeminjaman();
});