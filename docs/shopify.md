# Shopify 支持

## Filters

1. Array Filters
    - [x] concat
    - [x] join
    - [x] first
    - [x] index
    - [x] last
    - [x] map
    - [x] reverse
    - [x] size
    - [x] sort
    - [x] uniq
    - [x] where

2. Math Filters
    - [x] abs
    - [x] at_least
    - [x] at_most
    - [x] ceil
    - [x] divided_by
    - [x] floor
    - [x] minus
    - [x] plus
    - [x] round
    - [x] times
    - [x] modulo

3. Color Filters
    - [x] brightness_difference
    - [x] color_brightness
    - [x] color_contrast 少许误差可能是公式不对 [https://www.w3.org/TR/AERT/#color-contrast]
    - [x] color_darken
    - [x] color_desaturate
    - [x] color_difference
    - [x] color_extract
    - [x] color_lighten
    - [x] color_mix
    - [x] color_modify
    - [x] color_saturate
    - [x] color_to_rgb
    - [x] color_to_hsl
    - [x] color_to_hex

4. Money Filters
    - [ ] money
    - [ ] money_with_currency
    - [ ] money_without_trailing_zeros
    - [ ] money_without_currency

5. String Filters
    - [x] append
    - [x] camelcase
    - [x] capitalize
    - [x] downcase
    - [x] escape
    - [x] handleize
    - [x] hmac_sha1
    - [x] hmac_sha256
    - [x] md5
    - [x] newline_to_br
    - [x] pluralize
    - [x] prepend
    - [x] remove
    - [x] remove_first
    - [x] replace
    - [x] replace_first
    - [x] slice
    - [x] split
    - [x] strip
    - [x] lstrip
    - [x] reverse
    - [x] rstrip
    - [x] sha1
    - [x] sha256
    - [x] strip_html
    - [x] strip_newlines
    - [x] truncate
    - [x] truncatewords
    - [x] upcase
    - [x] url_encode
    - [x] url_escape
    - [x] url_param_escape

6. HTML Filters
    - [ ] currency_selector
    - [ ] img_tag
    - [ ] payment_button
    - [ ] payment_type_svg_tag
    - [ ] script_tag
    - [ ] stylesheet_tag

7. URL Filters
    - [ ] asset_img_url
    - [ ] asset_url
    - [ ] file_img_url
    - [ ] file_url
    - [ ] customer_login_link
    - [ ] global_asset_url
    - [ ] img_url
    - [ ] link_to
    - [ ] link_to_vendor
    - [ ] link_to_type
    - [ ] link_to_tag
    - [ ] link_to_add_tag
    - [ ] link_to_remove_tag
    - [ ] payment_type_img_url
    - [ ] shopify_asset_url
    - [ ] sort_by
    - [ ] url_for_type
    - [ ] url_for_vendor
    - [ ] within

8. General Filters
    - [x] date
    - [x] default :TODO: diot 不支持空对象
    - [ ] default_errors
    - [ ] default_pagination
    - [ ] format_address  :TODO: 按照国家输出
    - [x] highlight
    - [x] highlight_active
    - [x] json
    - [x] placeholder_svg_tag
    - [x] time_tag
    - [ ] weight_with_unit  :TOOD: 需要有标准单位

9. Media Filters
    - [ ] external_video_tag
    - [ ] external_video_url
    - [ ] img_tag
    - [ ] img_url
    - [ ] media_tag
    - [ ] model_viewer_tag
    - [ ] video_tag

## Tags

1. Control Flow Tags
    - [x] {% if %}
    - [x] {% elsif %} / {% else %}
    - [x] {% case %} / {% when %}
    - [x] {% unless %}
    - [x] {% and %}
    - [x] {% or %}

2. Iteration Tags
    - [x] {% for %}
    - [x] {% else %}
    - [x] {% break %}
    - [ ] {% continue %}
    - [x] {% cycle %}
    - [x] {% tablerow %}

3. Theme Tags
    - [x] {% echo %}
    - [x] {% include %}
    - [ ] {% form %}
    - [x] {% liquid %}
    - [ ] {% paginate %}
    - [x] {% raw %}
    - [ ] {% render %}
    - [x] {% section %}
    - [ ] {% style %}

4. Variable Tags
    - [x] {% assign %}
    - [x] {% capture %}
    - [x] {% increment %}
    - [x] {% decrement %}
