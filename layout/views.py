from django.shortcuts import render
from django.views import View


# Create your views here.

# Vertical 

class LightSidebarView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Light Sidebar"
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/vertical/layout-light-sidebar.html', greeting)


class CompactSidebarView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Compact Sidebar"
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/vertical/layout-compact-sidebar.html', greeting)


class IconSidebarView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Icon Sidebar"
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/vertical/layout-icon-sidebar.html', greeting)


class BoxWidthSidebarView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Boxed Width"
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/vertical/layout-boxed-width-sidebar.html', greeting)


class PreloaderSidebarView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Preloader "
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/vertical/layout-preloader-sidebar.html', greeting)


class ColoredSidebarView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Colored Sidebar"
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/vertical/layout-colored-sidebar.html', greeting)


class ScrollableSidebarView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Scollable "
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/vertical/layout-scrollable-sidebar.html', greeting)


# Horizontal

class HorizontalView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Horizontal Layout"
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/horizontal/layout-horizontal.html', greeting)


class LightTopbarHoriView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Horizontal Topbar Light"
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/horizontal/layout-hori-topbar-light.html', greeting)


class BoxedWidthHoriView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Horizontal Boxed Width"
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/horizontal/layout-hori-boxed-width.html', greeting)


class PreloaderHoriView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Horizontal Preloader Layout"
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/horizontal/layout-hori-preloader.html', greeting)


class ColoredheaderHoriView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Horizontal Topbar Colored"
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/horizontal/layout-hori-colored-header.html', greeting)


class ScrollableHoriView(View):
    def get(self, request):
        greeting = {}
        greeting['heading'] = "Horizontal Scrollable Layout"
        greeting['pageview'] = "Layouts"
        return render(request, 'layout/horizontal/layout-hori-scrollable.html', greeting)

