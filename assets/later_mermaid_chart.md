graph LR
%% Main Stages Title Groupings (Visual only, Mermaid groups flow naturally)

    %% -- EXTRACT, LOAD Stage --
    subgraph Stage_Extract_Load [Extract, Load]
        direction LR
        Sources(Sources<br/>Cloud Apps, Databases, Events, Files)
    end

    %% -- TRANSFORM Stage (Core dbt area) --
    subgraph Stage_Transform [Transform]
        direction LR

        Staging[Staging<br/>_stg_*_<br/>Cleanse, rename, cast columns]

        Intermediate[Intermediate optional<br/>_int_*_<br/>Join sources]

        Marts[Marts business ready<br/>_dim_* / fct_*_<br/>Specific, curated business view]
    end

    %% -- TRANSFORM OUTCOMES --
    subgraph Transform_Outcomes [Transform Outcomes]
        dashboards_reports(dashboards & reports)
        self_service_analytics(self service analytics)
    end

    %% -- EXPORT Stage --
    subgraph Stage_Export [Export]
        direction LR
        Operational_Analytics[Operational Analytics<br/>_oa_*_<br/>Sync back to tools]
    end

    %% -- EXPORT OUTCOME --
    subgraph Export_Outcomes [Export Outcomes]
        synced_tools(Synced tools)
    end

    %% -- CONNECTIONS --
    Sources --> Staging

    %% Main transformation flow
    Staging --> Marts

    %% Optional intermediate path
    Staging --> Intermediate
    Intermediate --> Marts

    %% Transformation outcomes
    Marts --> dashboards_reports
    Marts --> self_service_analytics

    %% Export path
    Marts --> Operational_Analytics
    Operational_Analytics --> synced_tools

    %% Styling (Optional)
    classDef layer fill:#f9f,stroke:#333,stroke-width:2px;
    classDef grouping fill:#e1f5fe,stroke:#0277bd,stroke-width:1px,stroke-dasharray: 5 5;
    classDef outcome fill:#fff9c4,stroke:#fbc02d,stroke-width:1px;

    class Sources,Staging,Intermediate,Marts,Operational_Analytics layer;
    class Stage_Extract_Load,Stage_Transform,Stage_Export,Transform_Outcomes,Export_Outcomes grouping;
    class dashboards_reports,self_service_analytics,synced_tools outcome;
