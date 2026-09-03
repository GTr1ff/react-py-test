import { Column } from '@/types/column';
import { Table } from '@/types/table';
import { faker } from '@faker-js/faker';

type CellValue = string | number | boolean | null | CellValue[] | { [key: string]: CellValue };
type Row = Record<string, CellValue>;

const NAME_HEURISTICS: Array<[RegExp, () => string]> = [
  // People
  [/first_name|given_name/, () => faker.person.firstName()],
  [/last_name|surname|family_name/, () => faker.person.lastName()],
  [/middle_name/, () => faker.person.middleName()],
  [/full_name/, () => faker.person.fullName()],
  [/username|user_name|^login$/, () => faker.internet.username()],
  [/password_hash|_hash$|^hash$/, () => faker.string.alphanumeric(60)],
  [/password/, () => faker.internet.password()],
  [/job_title|^title$|position/, () => faker.person.jobTitle()],
  [/gender|sex/, () => faker.person.sex()],

  // Contact
  [/email/, () => faker.internet.email()],
  [/phone|mobile|fax/, () => faker.phone.number()],
  [/url|website|homepage/, () => faker.internet.url()],
  [/domain/, () => faker.internet.domainName()],
  [/ip_address|^ip$/, () => faker.internet.ip()],
  [/mac_address/, () => faker.internet.mac()],
  [/user_agent/, () => faker.internet.userAgent()],

  // Location
  [/^location$/, () => faker.location.streetAddress()],
  [/street|^address$|address_line/, () => faker.location.streetAddress()],
  [/city/, () => faker.location.city()],
  [/state|province/, () => faker.location.state()],
  [/country/, () => faker.location.country()],
  [/zip|postal_code|postcode/, () => faker.location.zipCode()],
  [/latitude|^lat$/, () => String(faker.location.latitude())],
  [/longitude|^lng$|^lon$/, () => String(faker.location.longitude())],
  [/timezone/, () => faker.location.timeZone()],

  // Company/commerce
  [/company|organi[sz]ation|employer/, () => faker.company.name()],
  [/department/, () => faker.commerce.department()],
  [/product/, () => faker.commerce.productName()],
  [/sku/, () => faker.string.alphanumeric(8).toUpperCase()],
  [/currency_code|^currency$/, () => faker.finance.currencyCode()],
  [/iban/, () => faker.finance.iban()],
  [/account_number/, () => faker.finance.accountNumber()],
  [/credit_card/, () => faker.finance.creditCardNumber()],
  [/bitcoin|btc_address/, () => faker.finance.bitcoinAddress()],

  // Identifiers
  [/^uuid$|_uuid$|^guid$/, () => faker.string.uuid()],
  [/^slug$|_slug$/, () => faker.lorem.slug()],
  [/^token$|_token$|api_key/, () => faker.string.alphanumeric(32)],
  [/^key$|_key$/, () => faker.lorem.slug(2).replace(/-/g, '_')],
  [/^colou?r$|hex_colou?r/, () => faker.color.rgb()],

  // Content
  [/^description$|_description$/, () => faker.lorem.sentence()],
  [/^notes?$|_notes?$|^comment$|_comment$/, () => faker.lorem.paragraph()],
  [/^message$|^body$|^content$|_message$/, () => faker.lorem.sentence()],
  [/^reason$|_reason$/, () => faker.lorem.sentence()],
  [/^bio$|^biography$|^about$/, () => faker.person.bio()],
  [/^tags?$|^category$/, () => faker.lorem.word()],
  [/language/, () => faker.helpers.arrayElement(['en', 'fr', 'de', 'es', 'it', 'pt', 'ja', 'zh'])],
  [/locale/, () => faker.location.countryCode()],
  [/^unit$|_unit$|^uom$/, () => faker.helpers.arrayElement(['g', 'kg', 'ml', 'l', 'tsp', 'tbsp', 'cup', 'oz'])],
  [/instruction|^steps?$|_steps?$|direction/, () => faker.lorem.paragraphs(2)],

  // Status/type enums
  [/^status$|_status$/, () => faker.helpers.arrayElement(['active', 'inactive', 'pending', 'archived'])],
  [/^type$|_type$/, () => faker.helpers.arrayElement(['standard', 'premium', 'basic'])],
  [/^role$|_role$/, () => faker.helpers.arrayElement(['admin', 'user', 'guest', 'moderator'])],
];

// A bare `name` column takes its meaning from the entity it describes — a name
// on `users` is a person, on `recipes` it is not. Matched first against the
// column's own prefix (`author_name` -> "author"), then against the table name.
// First match wins, so keep specific patterns above general ones.
const ENTITY_NAME_HEURISTICS: Array<[RegExp, () => string]> = [
  // Roles/jobs — before people, so `role_name` is a job title not a person
  [/^roles?$|^jobs?$|^positions?$|title/, () => faker.person.jobTitle()],

  // People — `author(?!iz)` so `authorizations` is not treated as a person
  [
    /user|customer|employee|person|people|member|client|contact|staff|author(?!iz)|student|teacher|patient|applicant|candidate|subscriber|guest|driver|owner|manager|recipient|passenger/,
    () => faker.person.fullName(),
  ],

  // Food & drink
  [/ingredient/, () => faker.food.ingredient()],
  [/recipe|dish|meal|menu/, () => faker.food.dish()],
  [/fruit/, () => faker.food.fruit()],
  [/vegetable/, () => faker.food.vegetable()],
  [/spice|seasoning/, () => faker.food.spice()],
  [/meat/, () => faker.food.meat()],

  // Books & media
  [/book|publication|novel/, () => faker.book.title()],
  [/publisher/, () => faker.book.publisher()],
  [/song|track/, () => faker.music.songName()],
  [/album/, () => faker.music.album()],
  [/artist|band|musician/, () => faker.music.artist()],
  [/genre/, () => faker.music.genre()],

  // Animals
  [/dogs?\b|canine/, () => faker.animal.dog()],
  [/cats?\b|feline/, () => faker.animal.cat()],
  [/birds?\b/, () => faker.animal.bird()],
  [/fish/, () => faker.animal.fish()],
  [/horses?\b/, () => faker.animal.horse()],
  [/insects?\b|bugs?\b/, () => faker.animal.insect()],
  [/animal|pets?\b|species|breed/, () => faker.animal.type()],

  // Travel
  [/airline|carrier/, () => faker.airline.airline().name],
  [/airport/, () => faker.airline.airport().name],
  [/airplane|aircraft|planes?\b/, () => faker.airline.airplane().name],

  // Vehicles
  [/bicycles?\b|bikes?\b/, () => faker.vehicle.bicycle()],
  [/vehicle|^cars?$|automobile/, () => faker.vehicle.vehicle()],

  // Places
  [/location|office|site|venue|building|facility|warehouse/, () => faker.location.city()],
  [/city|town/, () => faker.location.city()],
  [/countr/, () => faker.location.country()],
  [/state|province|region/, () => faker.location.state()],

  // Commerce & organisations
  [/product|item|merchandise|^goods?$/, () => faker.commerce.productName()],
  [/department/, () => faker.commerce.department()],
  [
    /compan|organi[sz]ation|employer|vendor|supplier|brand|manufacturer|restaurant|hotel|store|shop|school|universit|team/,
    () => faker.company.name(),
  ],

  // Finance
  [/currenc/, () => faker.finance.currencyName()],
  [/account/, () => faker.finance.accountName()],
  [/transaction/, () => faker.finance.transactionType()],

  // Misc
  [/file|document|attachment/, () => faker.system.fileName()],
  [/branch/, () => faker.git.branch()],
  [/colou?r/, () => faker.color.human()],
  [/element|chemical/, () => faker.science.chemicalElement().name],
  [/unit|measure/, () => faker.science.unit().name],
];

// Plausible ranges for numeric columns
const NUMERIC_HEURISTICS: Array<[RegExp, (scale: number) => number]> = [
  [/salary|annual_pay|compensation/, (s) => faker.number.float({ min: 30000, max: 200000, fractionDigits: s })],
  [/wage|hourly_rate/, (s) => faker.number.float({ min: 15, max: 150, fractionDigits: s })],
  [/hours/, (s) => faker.number.float({ min: 0, max: 2000, fractionDigits: s })],
  [/budget/, (s) => faker.number.float({ min: 10000, max: 1000000, fractionDigits: s })],
  [/price|cost|amount|total|fee|balance|revenue/, (s) => faker.number.float({ min: 1, max: 5000, fractionDigits: s })],
  [/percent|_rate$|ratio|discount/, (s) => faker.number.float({ min: 0, max: 100, fractionDigits: s })],
  [/quantity|^count$|_count$|^qty$|stock/, () => faker.number.int({ min: 0, max: 500 })],
  [/^age$/, () => faker.number.int({ min: 18, max: 80 })],
  [/^year$|_year$/, () => faker.number.int({ min: 1990, max: 2026 })],
];

// Marker pairs used to keep ranges ordered (start <= end) within a row.
const RANGE_MARKERS: Array<[string, string]> = [
  ['start', 'end'],
  ['begin', 'end'],
  ['from', 'to'],
  ['clockin', 'clockout'],
  ['checkin', 'checkout'],
  ['min', 'max'],
  ['created', 'updated'],
];

function entityNameFor(hint: string): string | null {
  const normalized = hint.toLowerCase();
  for (const [pattern, generator] of ENTITY_NAME_HEURISTICS) {
    if (pattern.test(normalized)) {
      return generator();
    }
  }
  return null;
}

function generateNumber(column: Column): number {
  const columnName = column.name.toLowerCase();
  const scale = column.numericScale || 2;
  for (const [pattern, generator] of NUMERIC_HEURISTICS) {
    if (pattern.test(columnName)) {
      return generator(scale);
    }
  }
  return faker.number.float({ min: 0, max: 10000, fractionDigits: scale });
}

function generateDate(column: Column, withTime: boolean): string {
  const columnName = column.name.toLowerCase();

  let date: Date;
  if (/birth|^dob$|_dob$/.test(columnName)) {
    date = faker.date.birthdate();
  } else if (/due|expir|renew|next_|scheduled/.test(columnName)) {
    date = faker.date.future();
  } else {
    date = faker.date.past();
  }

  const iso = date.toISOString();
  return withTime ? iso : iso.split('T')[0];
}

// Postgres reports array columns as dataType "ARRAY" with no element type
// (information_schema does not expose it), so infer one from the column name
// and fall back to text.
function inferArrayElementType(column: Column): string {
  if (column.subDatatype) return column.subDatatype;

  const name = column.name.toLowerCase();
  if (/(^|_)ints?(_|$)|integer|_ids?$|employees|users|members|counts?/.test(name)) return 'integer';
  if (/uuid|guid/.test(name)) return 'uuid';
  if (/bool|flags?/.test(name)) return 'boolean';
  if (/dates?|timestamps?/.test(name)) return 'timestamp';
  return 'text';
}

function generateValue(column: Column, tableName: string): CellValue {
  if (column.isNullable && Math.random() < 0.1) return null;

  const type = column.dataType.toLowerCase().trim();

  // Arrays: PostgreSQL internal notation (_int4), SQL notation (integer[]),
  // or a bare "ARRAY" whose element type has to be inferred.
  const isArray =
    (type.startsWith('_') && type.length > 1) ||
    type.endsWith('[]') ||
    type === 'array' ||
    type === 'arraylist';

  if (isArray) {
    let elementType = type.startsWith('_')
      ? type.slice(1)
      : type.endsWith('[]')
        ? type.slice(0, -2)
        : inferArrayElementType(column);

    // Guard against a nested-array inference looping.
    if (elementType.startsWith('_') || elementType.endsWith('[]') || elementType === 'array') {
      elementType = 'text';
    }

    const element: Column = {
      ...column,
      dataType: elementType,
      isNullable: false,
      isAutoIncrement: false,
    };
    return Array.from({ length: faker.number.int({ min: 1, max: 3 }) }, () =>
      generateValue(element, tableName),
    );
  }

  if (type === 'date') {
    return generateDate(column, false);
  }
  if (type.includes('timestamp') || type === 'datetime' || type === 'datetime2') {
    return generateDate(column, true);
  }
  if (type.startsWith('time')) {
    return faker.date.past().toISOString().split('T')[1].split('.')[0];
  }
  if (type === 'interval' || type === 'timespan') {
    return `P${faker.number.int({ min: 1, max: 30 })}DT${faker.number.int({ min: 0, max: 23 })}H`;
  }
  if (
    type === 'integer' ||
    type === 'int' ||
    type === 'int2' ||
    type === 'int4' ||
    type === 'int8' ||
    type === 'bigint' ||
    type === 'big int' ||
    type === 'smallint' ||
    type === 'small int' ||
    type === 'mediumint' ||
    type === 'medium int' ||
    type === 'tinyint' ||
    type === 'tiny int' ||
    type === 'serial' ||
    type === 'smallserial' ||
    type === 'bigserial'
  ) {
    if (column.isAutoIncrement) return null;
    return Math.round(generateNumber({ ...column, numericScale: 0 }));
  }
  // Floating point stays a JSON number.
  if (
    type === 'real' ||
    type === 'float' ||
    type === 'float4' ||
    type === 'float8' ||
    type === 'double' ||
    type === 'double precision'
  ) {
    return generateNumber(column);
  }
  // Fixed-precision decimals serialize as strings to preserve precision,
  // matching the TypeScript type mapping.
  if (type === 'decimal' || type === 'numeric' || type === 'money' || type === 'smallmoney') {
    return generateNumber(column).toFixed(column.numericScale || 2);
  }
  if (
    type === 'character varying' ||
    type === 'varchar' ||
    type === 'character' ||
    type === 'char' ||
    type === 'bpchar' ||
    type === 'nvarchar' ||
    type === 'nchar' ||
    type === 'text' ||
    type === 'string' ||
    type === 'enum' ||
    type === 'xml'
  ) {
    return generateString(column, tableName);
  }
  if (type === 'boolean' || type === 'bool' || type === 'bit' || type === 'varbit' || type === 'bit varying') {
    return faker.datatype.boolean();
  }
  if (type === 'uuid' || type === 'guid' || type === 'uniqueidentifier') {
    return faker.string.uuid();
  }
  // Binary columns come across the wire as base64 strings.
  if (
    type === 'bytea' ||
    type === 'binary' ||
    type === 'varbinary' ||
    type === 'blob' ||
    type === 'longblob' ||
    type === 'mediumblob' ||
    type === 'tinyblob' ||
    type === 'image'
  ) {
    return faker.string.alphanumeric({ length: 32 });
  }
  // JSON columns are objects, matching the TypeScript type mapping.
  if (type === 'json' || type === 'jsonb' || type === 'hstore') {
    return { [faker.lorem.word()]: faker.lorem.word() };
  }
  if (type === 'cidr' || type === 'inet') {
    return faker.internet.ip();
  }
  if (type === 'macaddr' || type === 'macaddr8') {
    return faker.internet.mac();
  }
  if (type === 'pg_lsn' || type === 'txid_snapshot' || type === 'tsquery' || type === 'tsvector') {
    return faker.string.alphanumeric({ length: 16 });
  }

  return null;
}

function generateString(column: Column, tableName: string): string {
  const columnName = column.name.toLowerCase();

  for (const [pattern, generator] of NAME_HEURISTICS) {
    if (pattern.test(columnName)) {
      return truncate(generator(), column.maxLength);
    }
  }

  // Bare `name` / `*_name`: the meaning comes from the entity, not the column.
  // Prefer the column's own prefix (`author_name` on `books` is still a person),
  // then the table name, then neutral filler.
  const nameMatch = /^(?:(.*)_)?name$/.exec(columnName);
  if (nameMatch) {
    const prefix = nameMatch[1];
    const value = (prefix ? entityNameFor(prefix) : null) ?? entityNameFor(tableName);
    return truncate(value ?? faker.lorem.words({ min: 1, max: 3 }), column.maxLength);
  }

  // Fallback
  return truncate(faker.lorem.words({ min: 1, max: 3 }), column.maxLength);
}

// Trim to maxLength on a word boundary so values are not cut mid-word.
function truncate(value: string, maxLength: number): string {
  if (!maxLength || value.length <= maxLength) return value;
  const cut = value.slice(0, maxLength);
  const lastSpace = cut.lastIndexOf(' ');
  return (lastSpace > 0 ? cut.slice(0, lastSpace) : cut).trim();
}

function toCamelCase(input: string): string {
  const words = input.split('_').filter((w) => w.length > 0);
  if (words.length === 0) return input;
  const pascal = words
    .map((w) => w[0].toUpperCase() + w.slice(1).toLowerCase())
    .join('');
  return pascal[0].toLowerCase() + pascal.slice(1);
}

// Swap paired range values that came out backwards (end before start).
function orderRanges(row: Row): void {
  const keys = Object.keys(row);
  for (const [startMarker, endMarker] of RANGE_MARKERS) {
    for (const startKey of keys) {
      const lowerStart = startKey.toLowerCase();
      if (!lowerStart.includes(startMarker)) continue;
      const base = lowerStart.replace(startMarker, '');
      const endKey = keys.find(
        (k) => k.toLowerCase().includes(endMarker) && k.toLowerCase().replace(endMarker, '') === base,
      );
      if (!endKey) continue;
      const startValue = row[startKey];
      const endValue = row[endKey];
      if (
        (typeof startValue === 'string' && typeof endValue === 'string' && endValue < startValue) ||
        (typeof startValue === 'number' && typeof endValue === 'number' && endValue < startValue)
      ) {
        row[startKey] = endValue;
        row[endKey] = startValue;
      }
    }
  }
}

function generateRow(table: Table, rowIndex: number): Row {
  const row: Row = {};
  for (const column of table.columns) {
    const key = toCamelCase(column.name);
    row[key] = column.isAutoIncrement ? rowIndex + 1 : generateValue(column, table.name);
  }
  orderRanges(row);
  return row;
}

export function generateRows(table: Table, count = 10): Row[] {
  return Array.from({ length: count }, (_, i) => generateRow(table, i));
}