import { Component, Input, OnInit } from '@angular/core';
import { HostsService } from 'src/app/services/hosts.service';
import { ModalService } from 'src/app/components/modal/modalService';
import { IHost } from 'src/app/date/IHost';
import { FormControl } from '@angular/forms';

@Component({
    selector: 'app-welcome',
    templateUrl: './hosts.page.html',
})
export class HostsComponent implements OnInit {
    hosts: IHost[] = []

    hostnameModal = new FormControl('')
    usernameModal = new FormControl('')
    passwordModal = new FormControl('')

    constructor(private hostsService: HostsService, private modalService: ModalService) {

    }

    ngOnInit(): void {
        this.hostsService.getAllHosts().subscribe((res: any) => {
            this.hosts = res
        })
    }

    addHostModal(host: IHost) {
        this.hostnameModal.setValue(host.hostname)
        this.usernameModal.setValue(host.username)
        this.passwordModal.setValue(host.password)
    }

    getHostModal() {
        return {
            "hostname": this.hostnameModal.value,
            "username": this.usernameModal.value,
            "password": this.passwordModal.value
        }
    }

    deleteHost(host: IHost) {
        this.hostsService.deleteHost(host).subscribe((res) => console.log(res));
        this.hostsService.getAllHosts().subscribe((res: any) => {
            this.hosts = res
        })
    }
    

    openHost(host: IHost) {
        this.addHostModal(host);
        this.openModal('custom-modal-2')
    }

    addHost() {
        this.hostsService.addHosts(this.getHostModal()).subscribe((res: any) => {
            alert(res.Status == 'Ok' ? 'Хост добавлен' : 'Ошибка ' + res['Status'])
            console.log(res)

            this.hostsService.getAllHosts().subscribe((res: any) => {
                this.hosts = res

                this.closeModal('custom-modal-1');
                this.addHostModal(this.getHostModal());
                this.openModal('custom-modal-2');
            })

         })
        console.log('add host')


    }

    testConnection() {
        console.log('test connection')
        const currentHost = this.getHostModal()
        this.hostsService.testConnection(currentHost).subscribe((res: any) => { console.log(res); alert(res.Status == true ? 'Соединение установлено: ' + currentHost.hostname : 'Не удалось подключиться к серверу: ' + currentHost.hostname) })
    }


    openModal(id: string) {
        this.modalService.open(id);
    }

    closeModal(id: string) {
        this.modalService.close(id);
    }
}