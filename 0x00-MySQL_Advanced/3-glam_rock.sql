-- SQL script that lists all bands with Glam rock
-- Import this table dump: metal_bands.sql.zip

SELECT band_name, (IFNULL(SPLIT, '2022') - formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC
