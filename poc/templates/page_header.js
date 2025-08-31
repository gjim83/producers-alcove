{%- macro page_header(page_data) %}
        <!-- Title -->
        <h1 class="main-title">producers' alcove_</h1>

        <!-- Subtitle -->
        <h2 class="main-title subtitle">{{ page_data.subtitle }}</h2>

        <!-- Menu -->
        <div class="menu-container">
            <input id="clicker" type="checkbox" name="menu" style="opacity: 0;">
            <label for="clicker" class="menu-checkbox">
                <div class="menu-button" onclick="menuClick(this)">
                    <div class="bar1"></div>
                    <div class="bar2"></div>
                    <div class="bar3"></div>
                </div>
            </label>
            <div class="dropmenu">
            {%- for page in page_data.dropmenu_items %}
                <a href="{{ page.path }}">{{ page.display }}</a>
            {%- endfor %}
            </div>
        </div>
{%- endmacro %}
