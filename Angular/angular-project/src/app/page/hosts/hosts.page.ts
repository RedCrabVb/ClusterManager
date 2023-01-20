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
        this.hostsService.getAllHosts().subscribe((res: any) =>{
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

    openHost(host: IHost) {
        this.addHostModal(host);
        // this.formName.setValue('ddd');
        this.openModal('custom-modal-1')
    }

    addHost() {
        this.hostsService.addHosts(this.getHostModal()).subscribe((res) => console.log(res))
        console.log('add host')

        this.hostsService.getAllHosts().subscribe((res: any) =>{
            this.hosts = res
        })
    }

    testConnection() {
        console.log('test connection')

        this.hostsService.testConnection(this.getHostModal()).subscribe((res) => {console.log(res)})
    }


    openModal(id: string) {
        this.modalService.open(id);
    }

    closeModal(id: string) {
        this.modalService.close(id);
    }
}