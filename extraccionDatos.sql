
DROP TABLE IF EXISTS ofertasNov2022
select replace(rtrim(ltrim(titulo)), '"','') as text, rtrim(ltrim(replace(keywords, ', ', ','))) as label into ofertasNov2022 from ofertasEmpleo where year(fechaAlta)=2022 and month(fechaAlta)=11 and isnull(keywords,'')<>'' group by titulo, keywords order by 1

declare @text varchar(8000)
declare @keywords varchar(8000)
declare @label varchar(8000)

-- UNIFICA KEYWORDS (SIN REPETIR) DE OFERTAS CON EL MISMO TITULO PERO CON DISTINTAS KEYWORDS
declare CursorTextUnificar cursor for	
	select text, STRING_AGG(label,',') from ofertasNov2022 group by text having count(*) > 1

	open CursorTextUnificar
	fetch next from CursorTextUnificar into @text, @keywords
		while @@fetch_status = 0
			begin
			
				select @label = STRING_AGG(A.value, ',') from (
					select distinct(value) as value from STRING_SPLIT(@keywords, ',')
					) A 
				
				-- ACTUALIZA KEYWORDS CON TODOS LOS TÉRMINOS NO REPETIDOS
				update ofertasNov2022 set label = @label WHERE TEXT = @text				

				fetch next from CursorTextUnificar
				into @text, @keywords
			end
	close CursorTextUnificar
deallocate CursorTextUnificar

-- ELIMINA FILAS DUPLICADAS
select distinct * into ofertasNov2022_distinct from ofertasNov2022
delete from ofertasNov2022
insert into ofertasNov2022 select * from ofertasNov2022_distinct
drop table ofertasNov2022_distinct 


-- SELECCIÓN DE OFERTAS EN ORDEN ALEATORIO
select * from 
(
	SELECT 
	distinct '"' + label + '"' as label, '"' + text + '"'  as text
	FROM 
	ofertasNov2022
	where len(text) between 4 and 80
) A
ORDER BY NEWID()
