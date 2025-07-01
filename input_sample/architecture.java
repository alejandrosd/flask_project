architecture EvolvedArchitecture {
    component-and-connector-view::
        elements{
            component course_ms();
            component professor_ms(institution);
            connector http HTTP;
        }
        relations{
            attachment (HTTP:course_ms, professor_ms);
        }
}

-- data model view
-- TSL 

-> API -> SourceCode 