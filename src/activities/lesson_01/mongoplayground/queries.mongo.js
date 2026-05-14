/**
 * ===================================================================================================================
 * 1. Clientes con compras > 100€
 * -------------------------------------------------------------------------------------------------------------------
 * Accede al campo 'precio' dentro del Array de 'compras' de cada elemento. El operador '$gt' (greater than) filtra 
 * los elementos donde al menos uno cumple la condición
 */

db.collection.find({ "compras.precio": { $gt: 100 } })

/** 
 * ===================================================================================================================
 * 
 * 
 * 2. Nombre y ciudad de compradores de 'Portátil'
 * -------------------------------------------------------------------------------------------------------------------
 * Filtro directo sobre 'producto' en el Array del 'compras' de cada elemento y para la salida se indica con un 1 los
 * campos que queremos visualizar y con un 0 el campo _id para excluirlo
 */
db.collection.find({ "compras.producto": "Portátil" }, { "nombre": 1, "ciudad": 1, "_id": 0 });

/** 
 * ===================================================================================================================
 * 
 * 
 * 3. Clientes de Madrid con edad > 30
 * -------------------------------------------------------------------------------------------------------------------
 * Operador lógico '$and' para combinar dos criterios sobre los campos de cada elemento del Array raíz
 */
db.clientes.find({ $and: [ { "ciudad": "Madrid" }, { "edad": { $gt: 30 } } ] });

/** 
 * ===================================================================================================================
 * 
 * 
 * 4. Compras del cliente más joven
 * -------------------------------------------------------------------------------------------------------------------
 * Se ordena el Array de elementos por el campo o atributo 'edad' de forma ascendente (1) mediante 'sort' y se aplica
 * un 'limit' 1 para quedarnos únicamente con el primer registro de la lista ordenada
 */
db.clientes.find({}, { "compras": 1, "_id": 0 }).sort({ "edad": 1 }).limit(1);

/** 
 * ===================================================================================================================
 * 
 * 
 * 5. Clientes con al menos dos compras
 * -------------------------------------------------------------------------------------------------------------------
 * El operador '$where' permite aplicar una condición para evaluar la propiedad '.length' del atributo o campo 
 * compras como si de un objeto se tratase, por lo que según se pide en el ejercicio, se filtran los elementos 
 * cuyo Array de 'compras' tiene una longitud mayor o igual a 2
 */
db.clientes.find({ $where: "this.compras.length >= 2" });