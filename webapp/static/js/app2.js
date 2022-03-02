$(document).ready(function () {
    $('#input_file').on('change', function () {
        file = $('#input_file').prop('files')[0];
        var form_data = new FormData();
        form_data.append('file', file);

        $.ajax({
            url: '/api/process',
            type: "post",
            data: form_data,
            enctype: 'multipart/form-data',
            contentType: false,
            processData: false,
            cache: false,
            beforeSend: function () {
                $(".overlay").show()
            },
        }).done(function (jsondata, textStatus, jqXHR) {
            payload = jsondata
            
            // $('.pulse-button-container').remove()
            // for (i = 0; i < payload.bbox.length; i++) {
            //     x1 = payload.bbox[i][0]
            //     y1 = payload.bbox[i][1]
            //     x2 = payload.bbox[i][2]
            //     y2 = payload.bbox[i][3]
            //     x = x1 + ((x2 - x1) / 2) - 25
            //     y = y1 + ((y2 - y1) / 2) + 50

            //     obj = $('#pulse-x').clone().attr('id', `pulse-${i}`).prependTo('.frame-container')
            //     $(`#pulse-${i}`).addClass('pulse-button-container').css({
            //         'left': x,
            //         'top': y,
            //         // 'display': 'block'
            //     })
            // }


            $('#img-product').attr('src', payload.img)

            $(".overlay").hide()
        }).fail(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
            $(".overlay").hide()
        });

    })
})