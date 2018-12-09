$(document).ready(function(){

  function calculatingBasketAmount(){
    var total_order_amount = 0;
    $('.total-product-in-basket-amount').each(function(){
      total_order_amount += parseFloat($(this).text());
    });
    $('#total_order_amount').text(total_order_amount.toFixed(2));
  };

  $(document).on('change', ".product-in-basket-nmb", function(){
    var current_nmb = $(this).val();
    var current_tr = $(this).closest('tr');
    var current_price = parseFloat(current_tr.find(".product-price").text()).toFixed(2);
    var total_amount = parseFloat(current_nmb * current_price).toFixed(2);
    current_tr.find(".total-product-in-basket-amount").text(total_amount);
    calculatingBasketAmount();
  });
    calculatingBasketAmount();

    function showingBasket(){
      $('.basket-items').toggleClass('hidden');
    };

    $('.basket-container').on('click', function(e){
      e.preventDefault();
      showingBasket();
    });

  function BasketUpdating(product_id, nmb, form, is_delete, is_fast){
    var data = {};
    var url = form.attr('action');
    console.log(url);
    var csrf_token = $('#basket-navbar-post [name="csrfmiddlewaretoken"]').val();
    data["csrfmiddlewaretoken"] = csrf_token;
    data.product_id = product_id;
    data.nmb = nmb;
    if (is_delete){
      data["is_delete"] = true;
    }
    if (is_fast){
      data["is_fast"] = true;
    }
    console.log(data);
    $.ajax({
      url: url,
      type: 'POST',
      data: data,
      cache: true,
      success: function(data){
        console.log("OK");
        console.log(data.products_total_nmb);
        $('#basket_total_nmb').text("(" + data.products_total_nmb + ")");
        $('.basket-items ul').html("");
        if (data.products_total_nmb){
          console.log(data.products);
          $.each(data.products, function(k, val){
            $('.basket-items ul').append('<li>' + val.name + ', ' + val.nmb + ' шт. по ' + val.price_per_item + ' руб.  ' +
              '<a class="delete-item" href="" data-product_id="' + val.id + '">x</a>' +
              '</li>');
          });

          if (document.querySelector('.basket-table') !== null) {
            var total_amount = 0;
            $('.basket-table tbody').html("");
            $.each(data.products, function(k, val){
              total_amount = parseFloat(val.nmb * val.price_per_item).toFixed(2);
              $('.basket-table tbody').append(
              '<tr>' +
              '<td>' + val.name + '</td>' +
              '<td>' + '<input value=' + val.nmb + ' type="number" onkeypress="return event.charCode >= 48" min="1" class="product-in-basket-nmb" name="product_in_basket_' + val.id + '">' + '</td>' +
              '<td>' + '<span class="product-price">' + val.price_per_item + '</span>' + '</td>' +
              '<td>' + '<span class="total-product-in-basket-amount">' + total_amount + '</span>' + '</td>' +
              '<td>' + '<a class="delete-item" href="" data-product_id = "' + val.id + '">x</a>' + '</td>' +
              '</tr>'
              );
              calculatingBasketAmount();
            });
          }
        }
        else {
          if (document.querySelector('.basket-info-post') !== null) {
            $('.basket-info-post').html("");
            $('.basket-info-post').append('<h3 class="text-center">В корзине нет товаров</h3>');
          }
        }
      },
      error: function(){
        console.log("Error");
      },
    });
  }

  // $('#form_buing_product').on('submit', function(e){
  //   e.preventDefault();
  //   var form = $('#form_buing_product');
  //   var nmb = $('#number').val();
  //   var submit_btn = $('#submit_btn');
  //   var product_id = submit_btn.data("product_id");
  //   var product_name = submit_btn.data("name");
  //   var product_price = submit_btn.data("price");
  //   console.log(form);
  //   // BasketUpdating(product_id, nmb, form, is_delete = false, is_fast = true);
  // });

  $(document).on('click', '.add-basket-product', function(e){
    e.preventDefault();
    var form = $('#form_buing_product');
    var nmb = $('#number').val();
    var product_id = $(this).data("product_id");
    var product_name = $(this).data("product_name");
    var product_price = $(this).data("price");
    BasketUpdating(product_id, nmb, form, is_delete = false, is_fast = false);
  });

  $(document).on('click', '.add-basket-item', function(e){
    e.preventDefault();
    var form = $('#basket-navbar-post');
    var nmb = $(this).data("number");
    var product_id = $(this).data("product_id");
    var product_name = $(this).data("product_name");
    var product_price = $(this).data("price");
    BasketUpdating(product_id, nmb, form, is_delete = false, is_fast = false);
  });

  $(document).on('click', '.delete-item', function(e){
    e.preventDefault();
    var form = $('#basket-navbar-post');
    var product_id = $(this).data("product_id");
    var nmb = 0;
    BasketUpdating(product_id, nmb, form, is_delete = true, is_fast = false);
  });


    // $('.basket-container').on('mouseover', function(){
    //   showingBasket();
    // });
    // $('.basket-container').on('mouseout', function(){
    //   showingBasket();
    // });

});
