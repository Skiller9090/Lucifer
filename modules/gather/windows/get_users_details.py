from modules.gather.windows import get_users

from LMI.Command import return_output
from LMI.Table import generate_table, dictionary_max_transformation
from modules.Module import BaseModule


class Module(BaseModule):
    def run(self):
        userDetails = get_users.Module(self.luciferManager).run()
        local, domain = userDetails[0], userDetails[1]
        local_users = []
        domain_users = []
        for x in local:
            for u in x:
                local_users.append(u)
        for x in domain:
            for u in x:
                domain_users.append(u)
        local_users = self.get_user_details(local_users)
        domain_users = self.get_user_details(domain_users)

        for local in local_users:
            local = dictionary_max_transformation(local, max_chars=30)
            print(generate_table(list(zip(local.keys(), local.values())),
                                 headings=["Key", "Value"],
                                 title=f"Local - {local['User name']}"))
        for domain in domain_users:
            domain = dictionary_max_transformation(domain, max_chars=30)
            print(generate_table(list(zip(domain.keys(), domain.values())),
                                 headings=["Key", "Value"],
                                 title="Domain"))

    @staticmethod
    def get_user_details(users, domain=False):
        command = ["net", "user"]
        if domain:
            command.append("/domain")
        user_list = []
        for u in users:
            output = return_output([*command, u])
            detail_list = [x.split("     ") for x in output.split("\n")]
            for line in detail_list:
                while "" in line:
                    line.remove("")
                for i, cell in enumerate(line):
                    line[i] = cell.replace("\r", "").rstrip().strip()
            while [''] in detail_list:
                detail_list.remove([''])
            userdict = {}
            for detail in detail_list[:-2]:
                k, v = detail[0], "\n".join(detail[1:])
                userdict[k] = v
            user_list.append(userdict)
        return user_list
