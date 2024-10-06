export default [
    {
        title: 'Inicio',
        to: { name: 'index' },
        icon: { icon: 'tabler-smart-home' },
        action: "manage",
        subject: "index",
    },
    {
        title: "General",
        icon: { icon: "tabler-air-balloon" },
        action: "manage",
        subject: "pascking",
        children: [
            {
                title: 'País',
                to: { name: 'general-pais-pais' },
                action: "manage",
                subject: "general_pais",
            },
            {
                title: 'Moneda',
                to: { name: 'general-moneda-moneda' },
                action: "manage",
                subject: "general_moneda",
            },
            {
                title: 'Empresa',
                to: { name: 'general-empresa-empresa' },
                action: "manage",
                subject: "general_empresa",
            },
            {
                title: 'Departamento',
                to: { name: 'general-departamento-departamento' },
                action: "manage",
                subject: "general_departamento",
            },
            {
                title: 'Provincia',
                to: { name: 'general-provincia-provincia' },
                action: "manage",
                subject: "general_provincia",
            },
            {
                title: 'Distrito',
                to: { name: 'general-distrito-distrito' },
                action: "manage",
                subject: "general_distrito",
            },
        ],
        
    },
    {
        title: "Logistica",
        icon: { icon: "tabler-tir" },
        action: "manage",
        subject: "pascking",
        children: [
            {
                title: 'Centro',
                to: { name: 'logistica-centro-centro' },
                action: "manage",
                subject: "logistica_centro",
            },
            {
                title: 'Almacén',
                to: { name: 'logistica-almacen-almacen' },
                action: "manage",
                subject: "logistica_almacen",
            },
            {
                title: 'Proveedor',
                to: { name: 'logistica-proveedor-proveedor' },
                action: "manage",
                subject: "logistica_proveedor",
            },
            {
                title: 'Grupo',
                to: { name: 'logistica-grupo-grupo' },
                action: "manage",
                subject: "logistica_grupo",
            },
            {
                title: 'Subgrupo',
                to: { name: 'logistica-subgrupo-subgrupo' },
                action: "manage",
                subject: "logistica_subgrupo",
            },
            {
                title: 'Producto',
                to: { name: 'logistica-producto-producto' },
                action: "manage",
                subject: "logistica_producto",
            },
            {
                title: 'Movimiento',
                to: { name: 'logistica-movimiento-movimiento' },
                action: "manage",
                subject: "logistica_movimiento",
            },
            {
                title: 'Documento',
                to: { name: 'logistica-documento-documento' },
                action: "manage",
                subject: "logistica-documento",
            },
        ],
        
    },
    {
        title: "Agricola",
        icon: { icon: "tabler-shovel-pitchforks" },
        action: "manage",
        subject: "pascking",
        children: [
            {
                title: 'Campaña',
                to: { name: 'agricola-campania-campania' },
                action: "manage",
                subject: "agricola-campania",
            },
            {
                title: 'Cultivo',
                to: { name: 'agricola-cultivo-cultivo' },
                action: "manage",
                subject: "agricola_cultivo",
            },
            {
                title: 'Variedad',
                to: { name: 'agricola-variedad-variedad' },
                action: "manage",
                subject: "agricola_variedad",
            },
        ],
        
    },
    {
        title: "Historial",
        icon: { icon: "tabler-clock-record" },
        action: "manage",
        subject: "pascking",
        children: [
            {
                title: 'Auditoria',
                to: { name: 'historial-auditoria-auditoria' },
                action: "manage",
                subject: "agricola-campania",
            },
        ],
        
    },
]

/**  {
        title: "Travel Log",
        icon: { icon: "tabler-smart-home" },
        action: "manage",
        subject: "pascking",
        children: [
            {
                title: 'Travels',
                to: { name: 'travel_log-travels-travellog' },
                action: "manage",
                subject: "travel_log",
            },
            {
                title: 'Travels Modes',
                to: { name: 'travel_log-travel_modes-travelmodes' },
                action: "manage",
                subject: "travel_travel_modes",
            },
            {
                title: 'Divisions',
                to: { name: 'travel_log-divisions-divisions' },
                action: "manage",
                subject: "travel_divisions",
            },
            {
                title: 'Entities',
                to: { name: 'travel_log-entities-entities' },
                action: "manage",
                subject: "travel_entities",
            },
            {
                title: 'Nationalities',
                to: { name: 'travel_log-nationalities-nationalities' },
                action: "manage",
                subject: "travel_nationalities",
            },
            {
                title: 'Regions',
                to: { name: 'travel_log-regions-regions' },
                action: "manage",
                subject: "travel_regions",
            },
            {
                title: 'Countries',
                to: { name: 'travel_log-countries-countries' },
                action: "manage",
                subject: "travel_countries",
            },
        ]
    } */
