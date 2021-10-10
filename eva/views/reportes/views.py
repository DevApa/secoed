from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from authentication.models import Usuario
from eva.models import ResultadoProceso, Ciclo, ParametrosGeneral, Parametro


class ProcessResultEvaluations(TemplateView):
    template_name = 'reports/results/result.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_kpi(self):
        data = []

        coe_tic = 0.00
        coe_ped = 0.00
        coe_did = 0.00
        auto_tic = 0.00
        auto_ped = 0.00
        auto_did = 0.00

        n1 = 0.00
        n2 = 0.00
        n3 = 0.00
        n4 = 0.00

        yellow_traffic_light = ''
        traffic_light_orange = ''
        traffic_light_green = ''
        traffic_light_red = ''

        sat = ''
        sad = ''
        sap = ''
        sct = ''
        scd = ''
        scp = ''

        docente = Usuario.objects.filter(id=self.request.user.id).first()
        ciclo = Ciclo.objects.filter(is_active=True).first()
        parameter = Parametro.objects.filter(name='Indicadores').first()
        kpi = ParametrosGeneral.objects.filter(parameter=parameter.id)

        for ind in kpi:
            if ind.code == 'IND':
                n1 = float(ind.value)
            elif ind.code == 'RC':
                n2 = float(ind.value)
            elif ind.code == 'RCA':
                n3 = float(ind.value)
            elif ind.code == 'RCAI':
                n4 = float(ind.value)

        totals = ResultadoProceso.objects.filter(user=docente.id, cycle=ciclo.id).first()

        if totals is not None:
            coe_tic = float(totals.coe_result_Tic)
            coe_did = float(totals.coe_result_Did)
            coe_ped = float(totals.coe_result_Ped)

            auto_tic = float(totals.auto_result_Tic)
            auto_did = float(totals.auto_result_Did)
            auto_ped = float(totals.auto_result_Ped)

            if auto_ped <= n1:
                traffic_light_red = 'images/eva/rojo.png'
                sap = traffic_light_red
            elif auto_ped <= n2:
                traffic_light_orange = 'images/eva/naranja.png'
                sap = traffic_light_orange
            elif auto_ped <= n3:
                traffic_light_yellow = 'images/eva/amarillo.png'
                sap = traffic_light_yellow
            elif n3 < auto_ped <= n4:
                traffic_light_green = 'images/eva/verde.png'
                sap = traffic_light_green

            if auto_did <= n1:
                traffic_light_red = 'images/eva/rojo.png'
                sad = traffic_light_red
            elif auto_did <= n2:
                traffic_light_orange = 'images/eva/naranja.png'
                sad = traffic_light_orange
            elif auto_did <= n3:
                traffic_light_yellow = 'images/eva/amarillo.png'
                sad = traffic_light_yellow
            elif n3 < auto_did <= n4:
                traffic_light_green = 'images/eva/verde.png'
                sad = traffic_light_green

            if auto_tic <= n1:
                traffic_light_red = 'images/eva/rojo.png'
                sat = traffic_light_red
            elif auto_tic <= n2:
                traffic_light_orange = 'images/eva/naranja.png'
                sat = traffic_light_orange
            elif n2 < auto_tic <= n3:
                traffic_light_yellow = 'images/eva/amarillo.png'
                sat = traffic_light_yellow
            elif n3 < auto_tic <= n4:
                traffic_light_green = 'images/eva/verde.png'
                sat = traffic_light_green

            if coe_ped <= n1:
                traffic_light_red = 'images/eva/rojo.png'
                scp = traffic_light_red
            elif coe_ped <= n2:
                traffic_light_orange = 'images/eva/naranja.png'
                scp = traffic_light_orange
            elif n2 < coe_ped <= n3:
                traffic_light_yellow = 'images/eva/amarillo.png'
                scp = traffic_light_yellow
            elif n3 < coe_ped <= n4:
                traffic_light_green = 'images/eva/verde.png'
                scp = traffic_light_green

            if coe_did <= n1:
                traffic_light_red = 'images/eva/rojo.png'
                scd = traffic_light_red
            elif coe_did <= n2:
                traffic_light_orange = 'images/eva/naranja.png'
                scd = traffic_light_orange
            elif coe_did <= n3:
                traffic_light_yellow = 'images/eva/amarillo.png'
                scd = traffic_light_yellow
            elif n3 > coe_did <= n4:
                traffic_light_green = 'images/eva/verde.png'
                scd = traffic_light_green

            if coe_tic <= n1:
                traffic_light_red = 'images/eva/rojo.png'
                sct = traffic_light_red
            elif coe_tic <= n2:
                traffic_light_orange = 'images/eva/naranja.png'
                sct = traffic_light_orange
            elif coe_tic <= n3:
                traffic_light_yellow = 'images/eva/amarillo.png'
                sct = traffic_light_yellow
            elif n3 < coe_tic <= n4:
                traffic_light_green = 'images/eva/verde.png'
                sct = traffic_light_green

            auto_tic = {'semaforo_atic': sat}
            auto_ped = {'semaforo_aped': sap}
            auto_did = {'semaforo_adid': sad}
            coe_tic = {'semaforo_ctic': sct}
            coe_ped = {'semaforo_cped': scp}
            coe_did = {'semaforo_cdid': scd}

            data.append(auto_tic)
            data.append(auto_ped)
            data.append(auto_did)
            data.append(coe_tic)
            data.append(coe_ped)
            data.append(coe_did)
            return data

    def get_graph_co_evaluation_by_category(self):
        data = []
        try:
            docente = Usuario.objects.filter(id=self.request.user.id).first()
            ciclo = Ciclo.objects.filter(is_active=True).first()
            result_by_teacher = ResultadoProceso.objects.filter(user=docente.id, cycle=ciclo.id).values(
                'coe_result_Tic', 'coe_result_Did', 'coe_result_Ped').first()

            tic = ['Tics', float(result_by_teacher['coe_result_Tic'])]
            did = ['Didáctica', float(result_by_teacher['coe_result_Did'])]
            ped = ['Pedagógica', float(result_by_teacher['coe_result_Ped'])]

            data.append(tic)
            data.append(did)
            data.append(ped)
        except:
            pass
        return data

    def get_total_co_evaluation(self):
        total_coe = []
        try:
            docente = Usuario.objects.filter(id=self.request.user.id).first()
            ciclo = Ciclo.objects.filter(is_active=True).first()
            result = ResultadoProceso.objects.filter(user=docente.id, cycle=ciclo.id).values(
                'Total_Proceso_Coe').first()
            for r in result:
                tot = float(result['Total_Proceso_Coe'])
                total_coe.append(tot)
        except:
            pass
        return total_coe

    def get_total_auto_evaluation(self):
        total_auto = []
        try:
            docente = Usuario.objects.filter(id=self.request.user.id).first()
            ciclo = Ciclo.objects.filter(is_active=True).first()
            result = ResultadoProceso.objects.filter(user=docente.id, cycle=ciclo.id).values(
                'Total_Proceso_Auto').first()
            for r in result:
                tot = float(result['Total_Proceso_Auto'])
                total_auto.append(tot)
        except:
            pass
        return total_auto

    def get_total_auto(self):
        result = None
        try:
            docente = Usuario.objects.filter(id=self.request.user.id).first()
            ciclo = Ciclo.objects.filter(is_active=True).first()
            result = ResultadoProceso.objects.filter(user=docente.id, cycle=ciclo.id).first()
        except:
            pass
        return result

    def get_graph_auto_evaluation_by_category(self):
        data = []
        try:
            docente = Usuario.objects.filter(id=self.request.user.id).first()
            ciclo = Ciclo.objects.filter(is_active=True).first()
            result_by_teacher = ResultadoProceso.objects.filter(user=docente.id, cycle=ciclo.id).values(
                'auto_result_Tic', 'auto_result_Did', 'auto_result_Ped').first()

            tic = ['Tics', float(result_by_teacher['auto_result_Tic'])]
            did = ['Didáctica', float(result_by_teacher['auto_result_Did'])]
            ped = ['Pedagógica', float(result_by_teacher['auto_result_Ped'])]

            data.append(tic)
            data.append(did)
            data.append(ped)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['heading'] = 'Reporte de proceso'
        cycle = Ciclo.objects.filter(is_active=True).first()
        context['pageview'] = cycle.name
        kpi = self.get_kpi()
        if kpi is not None:
            context['semaforo_atic'] = kpi[0]['semaforo_atic']
            context['semaforo_aped'] = kpi[1]['semaforo_aped']
            context['semaforo_adid'] = kpi[2]['semaforo_adid']
            context['semaforo_ctic'] = kpi[3]['semaforo_ctic']
            context['semaforo_cped'] = kpi[4]['semaforo_cped']
            context['semaforo_cdid'] = kpi[5]['semaforo_cdid']
        context['auto'] = self.get_total_auto()
        context['total_auto'] = self.get_total_auto_evaluation()
        context['total_coe'] = self.get_total_co_evaluation()
        context['graph_evaluation'] = self.get_graph_auto_evaluation_by_category()
        context['graph_co_evaluation'] = self.get_graph_co_evaluation_by_category()
        return context
