import jsyaml from "js-yaml";
import fs from "fs";
import { log } from "console";

const school = jsyaml.load(
  fs.readFileSync("./settings/school_names.yml", "utf8")
);

const club = jsyaml.load(fs.readFileSync("./settings/club_names.yml", "utf8"));

const entityNew = jsyaml.load(
  fs.readFileSync("./settings/entity_names.yml", "utf8")
);

const entityOld = school.concat(club);

const entityNewAll = entityNew.map((item) => {
  const entity = item;
  entity["TextCn"] = entityOld.find((item) => item.code === entity.Code)?.cn;
  return entity;
});

fs.writeFileSync("./settings/entity_names.yml", jsyaml.dump(entityNewAll));
