<template>
	<div
		class="marketplace-page"
		:data-page-name="page_name"
	>
		<h5>{{ page_title }}</h5>

		<item-cards-container
			:container_name="page_title"
			:items="items"
			:item_id_fieldname="item_id_fieldname"
			:on_click="go_to_item_details_page"
			:editable="true"
			@remove-item="on_item_remove"
			:empty_state_message="empty_state_message"
		>
		</item-cards-container>
	</div>
</template>

<script>
export default {
	name: 'saved-items-page',
	data() {
		return {
			page_name: dataent.get_route()[1],
			items: [],
			item_id_fieldname: 'name',

			// Constants
			page_title: __('Saved Items'),
			empty_state_message: __(`You haven't saved any items yet.`)
		};
	},
	created() {
		this.get_items();
	},
	methods: {
		get_items() {
			hub.call(
				'get_saved_items_of_user', {},
				'action:item_save'
			)
			.then((items) => {
				this.items = items;
			})
		},

		go_to_item_details_page(hub_item_name) {
			dataent.set_route(`marketplace/item/${hub_item_name}`);
		},

		on_item_remove(hub_item_name) {
			const grace_period = 5000;
			let reverted = false;
			let alert;

			const undo_remove = () => {
				this.toggle_item(hub_item_name);;
				reverted = true;
				alert.hide();
				return false;
			}

			const item_name = this.items.filter(item => item.hub_item_name === hub_item_name);

			alert = dataent.show_alert(__(`<span>${item_name} removed.
				<a href="#" data-action="undo-remove"><b>Undo</b></a></span>`),
				grace_period/1000,
				{
					'undo-remove': undo_remove.bind(this)
				}
			);

			this.toggle_item(hub_item_name, false);

			setTimeout(() => {
				if(!reverted) {
					this.remove_item_from_saved_items(hub_item_name);
				}
			}, grace_period);
		},

		remove_item_from_saved_items(hub_item_name) {
			epaas.hub.trigger('action:item_save');
			hub.call('remove_item_from_user_saved_items', {
				hub_item_name,
				hub_user: dataent.session.user
			})
			.then(() => {
				this.get_items();
			})
			.catch(e => {
				console.log(e);
			});
		},

		// By default show
		toggle_item(hub_item_name, show=true) {
			this.items = this.items.map(item => {
				if(item.name === hub_item_name) {
					item.seen = show;
				}
				return item;
			});
		}
	}
}
</script>

<style scoped></style>
