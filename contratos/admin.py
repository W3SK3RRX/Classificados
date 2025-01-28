from django.contrib import admin
from .models import Contrato, ContratoTemplate


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'contratante', 'contratado', 'valor', 'prazo_execucao', 'contrato_gerado')
    list_filter = ('status', 'prazo_execucao')
    search_fields = ('titulo', 'descricao')

    actions = ['gerar_pdf_contratos']

    def gerar_pdf_contratos(self, request, queryset):
        for contrato in queryset:
            contrato.salvar_contrato_pdf()  # Gera o PDF de contratos selecionados
        self.message_user(request, "PDFs gerados com sucesso.")
    
    gerar_pdf_contratos.short_description = "Gerar PDF para contratos selecionados"


@admin.register(ContratoTemplate)
class ContratoTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'padrao', 'criado_em')
    list_filter = ('padrao',)
    search_fields = ('nome',)
    ordering = ('-criado_em',)

    # Ações personalizadas
    actions = ['duplicar_template']

    def duplicar_template(self, request, queryset):
        """
        Duplica os templates selecionados.
        """
        for template in queryset:
            template.pk = None  # Cria um novo registro
            template.nome = f"{template.nome} (Cópia)"
            template.save()
        self.message_user(request, "Templates duplicados com sucesso.")
    duplicar_template.short_description = "Duplicar templates selecionados"
